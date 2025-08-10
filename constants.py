BASE_URL = "https://oldschool.runescape.wiki/api.php"
GE_URL = "https://secure.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item="

QUERY_PARAMS = {
    "action": "query",
    "format": "json",
    "list": "search",
    "srsearch": "",
    "srlimit": 3}
PARSE_PARAMS = {
    "action": "parse",
    "pageid": "",
    "format": "json",
    "prop": "wikitext"}
HEADERS = {"user-agent": "osrsge-price-calculator-project"}

DATA_PARAMS = ["name", "examine", "id", "exchange", "value", "highalch", "lowalch", "price"]