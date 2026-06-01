- Amazon DynamoDB is a fast, flexible, and fully managed NoSQL database service that supports document and key-value models.
- It provides consistent, single-digit millisecond latency at any scale and automatically partitions data across multiple servers.
- Each table requires a Primary Key (Partition Key and optional Sort Key) to uniquely identify items. Since it is schema-less, items in the same table can have different attributes.

task 1: create a new table
- search for DynamoDB in the console and click Create table
- configure table details:
  - Table name: Music
  - Partition key: Artist (String)
  - Sort key: Song (String)
- use default settings and click Create table, then wait for status to become Active

task 2: add data
- choose Explore items in the left menu, select the Music table, and click Create item
- create three items with different attributes to test NoSQL flexibility

task 3: modify an existing item
- select the item with Artist 'Psy' from the list and choose Actions -> Edit item
- change Year from 2011 to 2012 and click Save

task 4: query the table
- select the Music table under Explore items
- test Query (runs fast, uses keys):
  - Partition key (Artist): Psy
  - Sort key (Song): Equal to 'Gangnam Style'
- test Scan (slower, searches entire table):
  - expand Filters, set Attribute name = 'Year' (Number), Condition = 'Equal to', Value = 1971
- click Run for both to verify the results

task 5: delete the table
- choose Tables, select the Music table, and click Delete
- type 'confirm' 
