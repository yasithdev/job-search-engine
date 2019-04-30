# Job Search Engine
Specialized Search Engine for Jobs in Norfolk, including Crawler, Indexer and Search Interface

## Instructions

### Folder Structure
```
job-search-engine
  |--crawler                (all source code for crawler)
      |-- spiders             (parser and link follower code for each domain)
          |-- common.py         (code to convert relative dates (e.g. 3 hours ago) to absolute dates)
          |-- craigslist.py     (parser for craigslist)
          |-- oodle.py          (parser for oodle)
          |-- theladders.py     (parser for theladders)
      |-- pipelines.py        (preprocessing [CrawlerPipeline] and duplicate URL elimination [DuplicatesPipeline])
      |-- settings.py         (crawler configuration)
  |--data                   (crawled data in .txt format)
  |--webui                  (web search interface)
      |-- package.json      (web interface configuration [npm])
      |-- (other files)     (HTML and JS components)
  |--data.json              (final json after crawling + preprocessing)
  |--scrapy.cfg             (default scrapy config file)
  |--update_index.py        (code to create indexes in elasticsearch and add documents to it)
```

### Prerequisites
* Python (version 3.x)
* NodeJS (version 10.x or greater)
* npm

(python, node and npm should be added to path)

### Cloning the Repository
```bash
git clone git@github.com:yasithmilinda/job-search-engine.git      `# using SSH`
git clone https://github.com/yasithmilinda/job-search-engine.git  `# using HTTPS`
```

### Crawling and Indexing
```bash
# installing dependencies
pip3 install scrapy

# running
scrapy crawl oodle          `# run oodle crawl`
scrapy crawl craigslist     `# run craigslist crawl`
scrapy crawl theladders     `# run theladders crawl`
./update_index.py           `# index in elasticsearch`
```

### Running the Search Interface
```bash
cd webui/       `# goto webui folder`

# installing dependencies
npm install     `# install dependencies in package.json`

# running
npm run start   `# start local web server (port: 3000)`
```
