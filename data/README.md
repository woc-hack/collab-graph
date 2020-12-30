# Retrieving the data from WoC

The data available through WoC infrastructure, gives a unique opportunity to have access to the whole OSS data at the same time which is vital to our goal. Here is how we have tried to use WoC.

### Trying to find the graph edges given a certain node

A sample commit: dddff9a89ddd7098a1625cafd3c9d1aa87474cc7

Using shell to find the author, piping the results to lookup a2p and then using results to lookup p2a:

`echo dddff9a89ddd7098a1625cafd3c9d1aa87474cc7 | ~/lookup/showCnt commit | cut -d \; -f 4 | ~/lookup/getValues -f a2p | cut -d \; -f 2 | ~/lookup/getValues -f p2a | cut -d \; -f 2 | sort | uniq`

Sample result:

    aaron <aaron@ccf9f872-aa2e-dd11-9fc8-001c23d0bc1f>
    aaron <aaron@FreeBSD.org>
    Aaron Dalton <aaron@ccf9f872-aa2e-dd11-9fc8-001c23d0bc1f>
    Aaron Dalton <aaron@FreeBSD.org>
    abial <abial@ccf9f872-aa2e-dd11-9fc8-001c23d0bc1f>
    abial <abial@FreeBSD.org>
    Achim Leubner <achim@ccf9f872-aa2e-dd11-9fc8-001c23d0bc1f>
    Achim Leubner <achim@FreeBSD.org>
    adam <adam@ccf9f872-aa2e-dd11-9fc8-001c23d0bc1f>
    adam <adam@FreeBSD.org>

This was just a demonstration, how to lookup authors connected to a given author.

But to start our search, we have to obtain a list of authors. For this purpose, we can use mongodb to retrieve the list of projects with at least two authors. Then using a p2a, we will have a complete list of authors who have participated in a project with at least one other author.

# 1. Building the whole graph

## 1.1. Obtaining the authors list (graph nodes)

### Finding projects with at least 2 authors

Using mongodb to retrieve list of projects with at least 2 authors.

    import pymongo
    import bson

    client = pymongo.MongoClient("mongodb://da1.eecs.utk.edu/")
    db = client ['WoC']
    coll = db['proj_metadata.R']

    dataset = coll.find( { "NumAuthors": { "$gt": 1 } } , {"projectID" : 1} , no_cursor_timeout=True )

    with open('./project_list', 'w') as f:
        for data in dataset:
            print >> f, data

    dataset.close()

Sample result:

    {u'projectID': u'akudryashov_SegmentControl', u'_id': ObjectId('5f8097d6316a1fef66927fe7')}
    {u'projectID': u'rads-io_open_data_schema_map', u'_id': ObjectId('5f8097d6316a1fef66927fe8')}
    {u'projectID': u'jon-acker_requirejs-di-mocks-example', u'_id': ObjectId('5f8097d6316a1fef66927fe9')}
    {u'projectID': u'xialiu1988_Songr', u'_id': ObjectId('5f8097d6316a1fef66927fea')}
    {u'projectID': u'ashwaniks_go-demo-3', u'_id': ObjectId('5f8097d6316a1fef66927feb')}

By the way, running this code results in the following error:

    Traceback (most recent call last):
      File "project_list.py", line 11, in <module>
        for data in dataset:
      File "/usr/lib64/python2.7/site-packages/pymongo/cursor.py", line 814, in next
        if len(self.__data) or self._refresh():
      File "/usr/lib64/python2.7/site-packages/pymongo/cursor.py", line 776, in _refresh
        limit, self.__id))
      File "/usr/lib64/python2.7/site-packages/pymongo/cursor.py", line 733, in __send_message
        response['starting_from'], self.__retrieved))
    AssertionError: Result batch started from 232103, expected 232102

But apparently this error is a BUG in Mongo (When querying a sharded replica set, Mongo returns an incorrect value for 'starting_from') and we got around it by running python with `-O` option which ignores assertion errors.

There are total number of **21,978,139** projects with more than one author which are now saved in *project_list*.

### Finding authors using the projects list

Using the project_list, list of authors was retrieved.

    cat project_list |
    cut -d \' -f 4 |
    ~/lookup/getValues -f p2a \
    > p2a_table \
    2> p2a_table.error

This query resulted in **62,067,751** rows.

Sample result:

    akudryashov_SegmentControl;Anton Kudryashov <qubabox@mail.ru>
    akudryashov_SegmentControl;Антон Кудряшов <qubabox@mail.ru>
    rads-io_open_data_schema_map;Aaron Couch <acinternets@gmail.com>
    rads-io_open_data_schema_map;Dan Feder <dafeder@gmail.com>
    rads-io_open_data_schema_map;Dan Feder <dan@nuams.com>

There were also **302** projects which could not be found with p2a mappings and are saved in *p2a_table.error*.

Using p2a_table we can obtain unique authors involved in our selected projects.

    cat p2a_table |
    cut -d \; -f 2 |
    sort |
    uniq -c |
    sed -n 's/^ *//g ; s/ /\;/p' \
    > author_list

That resulted in **25,880,258** unique authors.

#### Issues:

- Multiple names/emails associated with one author
- Invalid entries (e.g. "^_^ <^_^>")

To address auhtor ID resolution problem, we have tried to use a2A mappings:

    cat author_list |
    cut -d \; -f 2 |
    ~/lookup/getValues -f a2A \
    > a2A_table \
    2> a2A_table.error ;

That resulted in **14,517,517** errors which means we were only able to find about **11 million** author IDs in a2A mappings. These records aggregate into **5 million** unique Authors.

So to sum up, from 25 million unique author IDs, we were able to find 5 million unique Authors plus 14 million other IDs which weren't recognized. That means we have to **19 million** unique Authors.

As for the next step, we tried filtering out irrelevant author IDs by filtering out invalid email addresses using regular expressions.

    egrep '<[A-Za-z0-9._%+-]{1,}@[A-Za-z0-9.-]{1,}\.[A-Za-z]{2,}>$'

This reduced our author ID records about 2 million. *a2A_table* was updated accordingly.

Finally, using all the data we build our *p2A_table* which contains **47,400,507** rows of unique project name and Author combinations, containing **21,838,782** unique projects and **17,640,565** unique Authors.

# 2. Building a subset of graph given a certain node

Visualizing a graph this large with 18 million nodes is quit challenging. That made us consider visualizing subsets of the graph, based on a given node. The idea is to build a graph centered on a given node (Author) with requested depth, defined as the maximum distance between the central node and any given node in the graph.

Details can be found in a2gr directory.

