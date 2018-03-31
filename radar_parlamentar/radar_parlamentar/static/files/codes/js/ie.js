//JavaScript Patches for IE8- browsers

(function($){
        $(document).ready(function(){

                $('.miniBlogList').each(function(){
                        $(this).find('>li').last().css({'padding-bottom': 0, 'border-bottom': 'none'});
                });
                $('.blogList').find('.btmMeta').find('ul').find('li:last').css({
                                                                                                                                        'border': 'none',
                                                                                                                                        'padding-left': '10px',
                                                                                                                                        'padding-right': 0
                });
                $('.topMeta').find('li:last').css({
                                                                                'border': 'none',
                                                                                'padding-right': 0
                });
                $('#comments').find('>ul').each(function(){
                        $(this).find('>li:last').css({
                                                                                'border': 'none',
                                                                                'padding-bottom': 0
                                                                        })
                });
                $('#comments').find('.children').each(function(){
                        $(this).find('li:last').css({
                                                                                'border-bottom': 'none',
                                                                                'padding-bottom': 0
                                                                        })
                });
                
        });
})(jQuery);

/*

                #comments>ul>li:last-child,             
                #comments .children li:last-child{
                        border: none;
                        padding-bottom: 0;
                }

*/