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
    }
}