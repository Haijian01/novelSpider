settings = {
    'shuquge' : {
        'searchUrl' : 'http://www.shuquge.com/search.php',
        'searchFormKey' : 'searchkey',
        'searchResultNovelUrlListXpath' : '//div[@class="bookcase"]//h4[@class="bookname"]/a/@href',
        'searchResultNovelNameListXpath' : '//div[@class="bookcase"]//h4[@class="bookname"]/a/text()',
        'homeUrl' : 'http://www.shuquge.com',
        'novelNameXpath' : '//div[@class="book"]/div/h2/text()',
        'chapterNameXpath' : '//div[@class="book reader"]/div[@class="content"]/h1/text()',
        'viewContentXpath' : '//div[@class="content"]/div[@id="content"]/text()',
        'removeSpecialSymbolsInViewContent' : '\xa0',
        'chapterUrlListXpath' : '//div[@class="listmain"]//dt[2]/following-sibling::dd/a/@href',
        'chapterNameListXpath' : '//div[@class="listmain"]//dt[2]/following-sibling::dd/a/text()'
    },
    'soshuw' : {
        'searchUrl' : 'https://www.soshuw.com/search.html',
        'searchFormKey' : 'searchkey',
        'searchResultNovelUrlListXpath' : '//div[@class="novelslist2"]//ul/li/following-sibling::li/span[2]/a/@href',
        'searchResultNovelNameListXpath' : '//div[@class="novelslist2"]//ul/li/following-sibling::li/span[2]/a/text()',
        'homeUrl' : 'https://www.soshuw.com',
        'novelNameXpath' : '//div[@class="xiaoshuo"]/h1/text()',
        'chapterNameXpath' : '//div[@class="read_title"]/h1/text()',
        'viewContentXpath' : '//div[@class="read"]/div[@class="content"]/text()',
        'removeSpecialSymbolsInViewContent' : '\xa0',
        'chapterUrlListXpath' : '//div[@class="novel_list"][2]/dl/dd/a/@href',
        'chapterNameListXpath' : '//div[@class="novel_list"][2]/dl/dd/a/text()'
    }
}