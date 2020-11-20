# collab-graph

Members:
- Vladimir
- Nikolai
- Elena
- Mahmoud

Project info:

- team name: Collab-Graph
- Google meet / zoom room: https://meet.google.com/dsd-ohcj-xrf
- Working hours: late evenings (tentatively, 8 / 8:30 pm onwards) 

- Research questions: not questions, but deliverables:
1. Build a graph of collaboration between individuals across all OSS (Aggregate contributions per repository / file)
2. Build a usable and fun-to-explore tool (Static (?) web app with search and visualization) 
3. Provide a convenient way to work with the graph (Distribute a dump of a graph DB (e.g. neo4j))

# Trying to find the graph edges given a certain node

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

### Issues:

- Multiple names/emails associated with one author

But to start our search, we have to obtain a list of authors. For this purpose, we can use mongodb to retrieve the list of projects with at least two authors. Then using a p2a, we will have a complete list of authors who have participated in a project with at least one other author.

# Obtaining the authors list (graph nodes)

## Finding projects with at least 2 authors

Using mongodb to retrieve list of projects with at least 2 authors.

    coll = db['proj_metadata.R']
     
    dataset = coll.find( { "NumAuthors": { "$gt": 1 } } , {"projectID" : 1} )

Sample result:

    {u'projectID': u'akudryashov_SegmentControl', u'_id': ObjectId('5f8097d6316a1fef66927fe7')}
    {u'projectID': u'rads-io_open_data_schema_map', u'_id': ObjectId('5f8097d6316a1fef66927fe8')}
    {u'projectID': u'jon-acker_requirejs-di-mocks-example', u'_id': ObjectId('5f8097d6316a1fef66927fe9')}
    {u'projectID': u'xialiu1988_Songr', u'_id': ObjectId('5f8097d6316a1fef66927fea')}
    {u'projectID': u'ashwaniks_go-demo-3', u'_id': ObjectId('5f8097d6316a1fef66927feb')}

I cannot get the full list as I am getting this error right now:  

`AssertionError: Result batch started from 232103, expected 232102`

## Finding authors using the projects list

`cat project_list | head -1 | cut -d \' -f 4 | ~/lookup/getValues -f p2a`

Sample result:

    akudryashov_SegmentControl;Anton Kudryashov <qubabox@mail.ru>
    akudryashov_SegmentControl;Антон Кудряшов <qubabox@mail.ru>
    
### Issues:

- Multiple names/emails associated with one author
