var products= [];

$('.productThumbnail').each(function(){
    var id = $(this).attr('id');
	var src = $(this).find('.thumbnailImage').attr('src');
    var shortDesc = $(this).find('.shortDescription').find('a').html();
    //var shortDesc = shortDescWithExtra.replace(/\r?\n|\r/g, '');
    var $colorwayPrice = $(this).find('.colorway-price');
    var $prices = $colorwayPrice.find('.first-range');
    var prices = [];
    $prices.each(function(){
        var priceString = $(this).html();
        var priceWithExtra = priceString.replace( /^\D+/g, '');
        var price = priceWithExtra.replace(/\r?\n|\r/g, '');
    	prices.push(price);
    });
	var desc;
    if(shortDesc){
		desc = shortDesc.replace(/\r?\n|\r/g, '');
    }
    products.push({
		id: id,
		desc: desc,
        img: src,
        prices: prices
	});
});


var s = "";
for(i = 0; i < products.length; i++){
    s += JSON.stringify(products[i]) + ", " + '\n';
}
console.log(s);









var products = [];
var $items = $('.npr-gallery-item');
$items.each(function(){
    var img = $(this).find('img').attr('src');
    var $productTitle = $(this).find('.product-title');
    var title = $productTitle.find('a span').html();
    var price1 = $(this).find('.original-price .price').html();
    if(price1){
        price1 = price1.replace( /^\D+/g, '');
    }
    var price2 = $(this).find('.sale-price .price').html();
    if(price2){
        price2 = price2.replace( /^\D+/g, '');
    }
    products.push({
        desc: title,
        img: img,
        prices: [ price1, price2 ]
    });
});
var s = "";
for(i = 0; i < products.length; i++){
    s += JSON.stringify(products[i]) + ", " + '\n';
    
}
console.log(s);