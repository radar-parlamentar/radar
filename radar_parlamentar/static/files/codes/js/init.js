/* Site Initialization JS Codes + Some Third Party + Circle Theme Specific Plugins. */
/*
    ~"~"~ Circle ~"~"~ Responsive HTML5 & CSS3 Creative-Portfolio Theme by Nuruzzaman Sheikh (palpaldal)
    Please purchase a license from http://themeforest.net in order to use this template.
    Developer Web Address: http://www.palpaldal.com
    Themeforest profile: http://themeforest.net/user/palpaldal/

    Table of Contents
    ------------------
    1.  jQuery.easing plugin
    2.  jQuery.scrollTo plugin
    3.  jQuery.tinyValidator validates form fields then submits to server (with ajax methods).
    4.  jQuery.hidingLabel library script
    5.  jQuery.easySlider [a mini slider]
    6.  jQuery.tabSwitcher [a lean and tiny tab switching plugin]
    7.  jQuery.circlePortHover [a plugin to help this themes portfolio metas float on top of the thumbs]
    8.  jQuery.imagesLoaded plugin
    9.  jQuery.masonry plugin
    10. Theme Script initialization function
*/

/*
 * jQuery Easing v1.3 - http://gsgd.co.uk/sandbox/jquery/easing/
 *
 * Uses the built in easing capabilities added In jQuery 1.1
 * to offer multiple easing options
 *
 * TERMS OF USE - jQuery Easing
 *
 * Open source under the BSD License.
 *
 * Copyright © 2008 George McGinley Smith
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *
 * Redistributions of source code must retain the above copyright notice, this list of
 * conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright notice, this list
 * of conditions and the following disclaimer in the documentation and/or other materials
 * provided with the distribution.
 *
 * Neither the name of the author nor the names of contributors may be used to endorse
 * or promote products derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
 * EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 *  COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 *  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
 *  GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
 * AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 *  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
 * OF THE POSSIBILITY OF SUCH DAMAGE.
 *
*/

// t: current time, b: begInnIng value, c: change In value, d: duration
;
jQuery.easing['jswing'] = jQuery.easing['swing'];
jQuery.extend(jQuery.easing,{def: 'easeOutQuad',swing: function(x,t,b,c,d){return jQuery.easing[jQuery.easing.def](x, t, b, c, d);},easeInQuad:function(x,t,b,c,d){return c*(t/=d)*t+b;},easeOutQuad:function(x,t,b,c,d){return -c *(t/=d)*(t-2)+b;},easeInOutQuad:function(x,t,b,c,d){if((t/=d/2)<1)return c/2*t*t + b;return -c/2*((--t)*(t-2)-1)+b;},easeInCubic:function(x,t,b,c,d){return c*(t/=d)*t*t+b;},easeOutCubic:function(x,t,b,c,d){       return c*((t=t/d-1)*t*t+1)+b;},easeInOutCubic:function(x,t,b,c,d){if((t/=d/2)<1) return c/2*t*t*t+b;return c/2*((t-=2)*t*t+2)+b;},easeInQuart:function(x,t,b,c,d){return c*(t/=d)*t*t*t+b;},easeOutQuart:function(x,t,b,c,d){return -c*((t=t/d-1)*t*t*t-1)+b;},easeInOutQuart:function(x,t,b,c,d){if((t/=d/2)<1)return c/2*t*t*t*t+b;return -c/2*((t-=2)*t*t*t-2)+b;},easeInQuint:function(x,t,b,c,d){return c*(t/=d)*t*t*t*t+b;},easeOutQuint:function(x,t,b,c,d){return c*((t=t/d-1)*t*t*t*t+1)+b;},easeInOutQuint:function(x,t,b,c,d){if((t/=d/2)<1)return c/2*t*t*t*t*t+b;return c/2*((t-=2)*t*t*t*t+2)+b;},easeInSine:function(x,t,b,c,d){return -c*Math.cos(t/d*(Math.PI/2))+c+b;},easeOutSine:function(x,t,b,c,d){return c*Math.sin(t/d*(Math.PI/2))+b;},easeInOutSine:function(x,t,b,c,d){return -c/2*(Math.cos(Math.PI*t/d)-1)+b;},easeInExpo:function(x,t,b,c,d){return (t==0)?b:c*Math.pow(2,10*(t/d-1))+b;},easeOutExpo:function(x,t,b,c,d){return (t==d)?b+c:c*(-Math.pow(2,-10*t/d)+1)+b;},easeInOutExpo:function(x,t,b,c,d){if(t==0)return b;if(t==d)return b+c;if((t/=d/2)<1)return c/2*Math.pow(2,10*(t-1))+b;return c/2*(-Math.pow(2,-10*--t)+2)+b;}, easeInCirc:function(x, t, b, c, d){return -c*(Math.sqrt(1-(t/=d)*t)-1)+b;},easeOutCirc:function(x,t,b,c,d){return c*Math.sqrt(1-(t=t/d-1)*t)+b;},easeInOutCirc:function(x,t,b,c,d){if((t/=d/2)<1)return -c/2*(Math.sqrt(1-t*t)-1)+b;return c/2*(Math.sqrt(1-(t-=2)*t)+1)+b;},easeInElastic:function(x,t,b,c,d){var s=1.70158;var p=0;var a=c;if(t==0)return b;if((t/=d)==1)return b+c;if(!p)p=d*.3;if(a<Math.abs(c)){a=c;var s=p/4;}else var s=p/(2*Math.PI)*Math.asin(c/a);return -(a*Math.pow(2,10*(t-=1))*Math.sin((t*d-s)*(2*Math.PI)/p))+b;},easeOutElastic:function(x,t,b,c,d){var s=1.70158;var p=0;var a=c;if(t==0)return b;if((t/=d)==1)return b+c;if(!p)p=d*.3;if(a<Math.abs(c)){a=c;var s=p/4;}else var s=p/(2*Math.PI)*Math.asin(c/a);return a*Math.pow(2,-10*t)*Math.sin((t*d-s)*(2*Math.PI)/p)+c+b;},easeInOutElastic:function(x,t,b,c,d){var s=1.70158;var p=0;var a=c;if(t==0)return b;if((t/=d/2)==2)return b+c;if(!p)p=d*(.3*1.5);if(a<Math.abs(c)){a=c;var s=p/4;}else var s=p/(2*Math.PI)*Math.asin(c/a);if(t<1)return -.5*(a*Math.pow(2,10*(t-=1))*Math.sin((t*d-s)*(2*Math.PI)/p))+b;return a*Math.pow(2,-10*(t-=1))*Math.sin((t*d-s)*(2*Math.PI)/p)*.5+c+b;},easeInBack:function(x,t,b,c,d,s){if(s==undefined)s=1.70158;return c*(t/=d)*t*((s+1)*t-s)+b;},easeOutBack:function(x,t,b,c,d,s){if(s==undefined)s=1.70158;return c*((t=t/d-1)*t*((s+1)*t+s)+1)+b;},easeInOutBack:function(x,t,b,c,d,s){if(s==undefined)s=1.70158;if((t/=d/2)<1)return c/2*(t*t*(((s*=(1.525))+1)*t-s))+b;return c/2*((t-=2)*t*(((s*=(1.525))+1)*t+s)+2)+b;},easeInBounce:function(x,t,b,c,d){return c-jQuery.easing.easeOutBounce(x,d-t,0,c,d)+b;},easeOutBounce:function(x,t,b,c,d){if((t/=d)<(1/2.75)){return c*(7.5625*t*t)+b;}else if(t<(2/2.75)){return c*(7.5625*(t-=(1.5/2.75))*t+.75)+b;}else if(t<(2.5/2.75)){return c*(7.5625*(t-=(2.25/2.75))*t+.9375)+b;}else{return c*(7.5625*(t-=(2.625/2.75))*t+.984375)+b;}},easeInOutBounce:function(x,t,b,c,d){if(t<d/2)return jQuery.easing.easeInBounce(x,t*2,0,c,d)*.5+b;return jQuery.easing.easeOutBounce(x,t*2-d,0,c,d)*.5+c*.5+b;}});

/**
 * jQuery.ScrollTo - Easy element scrolling using jQuery.
 * Copyright (c) 2007-2009 Ariel Flesler - aflesler(at)gmail(dot)com | http://flesler.blogspot.com
 * Dual licensed under MIT and GPL.
 * Date: 3/9/2009
 * @author Ariel Flesler
 * @version 1.4.1
 *
 * http://flesler.blogspot.com/2007/10/jqueryscrollto.html
 */
;(function($){var m=$.scrollTo=function(b,h,f){$(window).scrollTo(b,h,f)};m.defaults={axis:'xy',duration:parseFloat($.fn.jquery)>=1.3?0:1};m.window=function(b){return $(window).scrollable()};$.fn.scrollable=function(){return this.map(function(){var b=this,h=!b.nodeName||$.inArray(b.nodeName.toLowerCase(),['iframe','#document','html','body'])!=-1;if(!h)return b;var f=(b.contentWindow||b).document||b.ownerDocument||b;return $.browser.safari||f.compatMode=='BackCompat'?f.body:f.documentElement})};$.fn.scrollTo=function(l,j,a){if(typeof j=='object'){a=j;j=0}if(typeof a=='function')a={onAfter:a};if(l=='max')l=9e9;a=$.extend({},m.defaults,a);j=j||a.speed||a.duration;a.queue=a.queue&&a.axis.length>1;if(a.queue)j/=2;a.offset=n(a.offset);a.over=n(a.over);return this.scrollable().each(function(){var k=this,o=$(k),d=l,p,g={},q=o.is('html,body');switch(typeof d){case'number':case'string':if(/^([+-]=)?\d+(\.\d+)?(px)?$/.test(d)){d=n(d);break}d=$(d,this);case'object':if(d.is||d.style)p=(d=$(d)).offset()}$.each(a.axis.split(''),function(b,h){var f=h=='x'?'Left':'Top',i=f.toLowerCase(),c='scroll'+f,r=k[c],s=h=='x'?'Width':'Height';if(p){g[c]=p[i]+(q?0:r-o.offset()[i]);if(a.margin){g[c]-=parseInt(d.css('margin'+f))||0;g[c]-=parseInt(d.css('border'+f+'Width'))||0}g[c]+=a.offset[i]||0;if(a.over[i])g[c]+=d[s.toLowerCase()]()*a.over[i]}else g[c]=d[i];if(/^\d+$/.test(g[c]))g[c]=g[c]<=0?0:Math.min(g[c],u(s));if(!b&&a.queue){if(r!=g[c])t(a.onAfterFirst);delete g[c]}});t(a.onAfter);function t(b){o.animate(g,j,a.easing,b&&function(){b.call(this,l,a)})};function u(b){var h='scroll'+b;if(!q)return k[h];var f='client'+b,i=k.ownerDocument.documentElement,c=k.ownerDocument.body;return Math.max(i[h],c[h])-Math.min(i[f],c[f])}}).end()};function n(b){return typeof b=='object'?b:{top:b,left:b}}})(jQuery);

/* JavaScript Custom Form Validation Routines

* It's functionality is so simple. It doesn't show any validation message until user first attempts to submit forms with inappropriately filled field. When user's try to submit the form for first time this script checks if every field has been filled properly othwerwise it prevents submission to the server and notifies user about her mistake(s). This time it validates each field as user focuses in and blurs them(fields) off.

* You can also change error messages if you like.
*/

;(function($){
    jQuery.fn.tinyValidator = function(options){
        var defaults = {
            emptyMsg: "This is a required field.",
            emailMsg: "Type a valid email address e.g. <code>john@domain.com</code>",
            urlMsg: "   Type proper url with \
                            <code>http://</code> portion \
                            or leave it blank<br /> \
                            e.g. &nbsp; <code>http://yourdomain.com</code><br /> \
                            <code>http://you.yourdomain.net</code>",
            sbtMsg: "Please, make sure you've properly filled all the above required fields.",
            ajax: false,
            miniForm : false,

            genError: function(field, msg){
                var holder = field.parent('li');
                if(!holder.hasClass('warning')){
                    holder.addClass('warning').append($('<p>' + msg + '</p>'));
                }
            },

            canError: function(field){
                var holder = field.parent('li');
                if(holder.hasClass('warning')){
                    holder.removeClass('warning').children('p').remove();
                }
            }
        };

        var opts = jQuery.extend(defaults, options);

        return this.each(function(){

            var form = jQuery(this);

            var ajaxMail = function(){
                //Get the data from all the fields
                var name = $('#name');
                var email = $('#email');
                var url = $('#url');
                var subject = $('#subject');
                var message = $('#message');
                //organize the data properly
                var data = 'name=' + name.val() + '&email=' + email.val() + '&url='+ url.val() + '&subject='+ subject.val() + '&message=' + message.val();

                //start the ajax
                $.ajax({
                    //this is the php file that processes the data and sends mail
                    url: "mail.php",
                    //GET method is used
                    type: "GET",
                    //pass the data
                    data: data,
                    //Do not cache the page
                    cache: false,
                    //success
                    success: function(html){
                        $('.sending', form.parent()).hide();
                        //if mail.php/mini-mail.php returned 1/true (send mail success)
                        if(html == 1){
                            $('.success', form.parent()).fadeTo('slow', 1);
                            setTimeout(function(){$('.success', form.parent()).fadeTo('slow', 0, function(){hideAll();});disable(false);}, 6000);
                        //if mail.php/mini-mail.php returned 0/false (send mail failed)
                        }
                        else{
                            $('.error', form.parent()).fadeTo('slow', 1);
                            setTimeout(function(){$('.error', form.parent()).fadeTo('slow', 0, function(){hideAll();}); disable(false);}, 6000);
                        }
                    }
                });
                //cancel the submit button default behaviours
                return false;
            };

            var hideAll = function(){
                $('.sending', form.parent()).hide();
                $('.success', form.parent()).hide();
                $('.error', form.parent()).hide();
            };

            var disable = function(disable){
                if(disable){
                    $('input, textarea, input[type=submit]', form).attr('disabled', 'true');
                    form.animate({opacity: .15}, 1000);
                }
                else{
                    $('input, textarea, input[type=submit]', form).removeAttr('disabled');
                    form.animate({opacity: 1}, 1000);
                }
            };

            form.one('submit', function(){
                jQuery(':input', form)
                    .filter('.empty')
                    .blur(function(){
                        if(this.value == '' || /^\s+$/.test(this.value)){
                            opts.genError(jQuery(this), opts.emptyMsg);
                        }
                        else{
                            opts.canError(jQuery(this));
                        }
                    })
                    .end()
                    .filter('.email')
                    .blur(function(){
                        if(this.value == '' || !/.+@.+\.[a-zA-Z]{2,4}$/.test(this.value)){
                            opts.genError(jQuery(this), opts.emailMsg);
                        }
                        else{
                            opts.canError(jQuery(this));
                        }
                    })
                    .end()
                    .filter('.url')
                    .blur(function(){
                        if((this.value == '' || /^\s+$/.test(this.value)) && jQuery(this).hasClass('optional')){
                            jQuery(this).val('');
                            opts.canError(jQuery(this));
                            return;
                        }
                        else if(this.value == '' || !/^(http|https):\/\/.+\.\w{2,4}$/.test(this.value)){
                            opts.genError(jQuery(this), opts.urlMsg);
                        }
                        else{
                            opts.canError(jQuery(this));
                        }
                    });
                }).submit(function(){
                    jQuery(':input', form).trigger('blur');
                    var warnings = jQuery('.warning', form).length;
                    var parent = jQuery(':submit', form).parent('li');
                    parent.find('p').remove();
                    if(warnings > 0){
                        parent.prepend(jQuery("<p><strong>" + opts.sbtMsg + "</strong></p>"));
                        return false;
                    }
                    else{
                        parent.find('p').remove();
                        if(opts.ajax){
                            $('.sending', form.parent()).fadeTo('slow', 1);
                            disable(true);
                            ajaxMail();
                            return false;
                        }
                        else{
                            return true;
                        }
                    }
            });
        });
    };
})(jQuery);

/* Form fields label hiding plugin */
;(function($){
    $.fn.hidingLabel = function(options){
        var fT = function(field){
            if(field.val() === '' || field.val() === ' '){
                field.siblings('label').fadeTo('slow', 0.4);
            }
        };
        var fB = function(field){
            if(field.val() === '' || field.val() === ' '){
                field.siblings('label').fadeTo('slow', 1);
            }
        };
        var h = function(field){
            if(field.val() !== '' || field.val() === ' '){
                field.siblings('label').hide();
            }
        };

        var autoCall = options;

        return this.each(function(){
            $(':text, :password, textarea', this).each(function(){
                var field = $(this);
                field.siblings('label').css('position', 'absolute');
                if(autoCall === true){
                    fB(field);
                }
                field.focus(function(){fT(field);})
                .keyup(function(){h(field);})
                .blur(function(){fB(field);});
                h(field);
            });
        });
    };
})(jQuery);


/* easySlider port featured portfolio or clients */
;(function($){
    $.fn.easySlider = function(options){

        return this.each(function(index){

        var defaults = {
            slides : 4, //items to be shown
            first : 'sFirst',//first slide class name
            last : 'sLast'//last slide class name
        }

        var opts = $.extend(defaults, options);

            var o = $(this);
            var btns = $('<a href="#" class="prevSBtn inactive">Previous</a> <a href="#" class="nextSBtn">Next</a>');

            o.append(btns);

            var right = opts.slides - 1; //last displayed item
            var objs = o.find('>li');
            var cardWidth = objs.outerWidth(true);
            var total = objs.length;
            var prvBtn = o.parent().find('.prevSBtn');
            var nxtBtn = o.parent().find('.nextSBtn');
            var clc = 0; //clear left counter
            var crc = 0; //clear right counter

            if(right >= total-1){
                prvBtn.hide();
                nxtBtn.hide();
            }

            var clearRight = function(){
                crc++;
                if(crc == total){
                    objs.filter('.'+opts.last).removeClass(opts.last).hide().prev().addClass(opts.last);
                    crc = 0;
                }
                else{return false;}
            };

            var clearLeft = function(){
                clc++;
                if(clc == total){
                    objs.filter('.'+opts.first).removeClass(opts.first).hide().next().addClass(opts.first);
                    clc = 0;
                }
                else{return false;}
            };

            objs.each(function(index){
                var dis = $(this);
                var left = dis.prevAll().length * cardWidth;
                dis.css({'position': 'absolute', 'left': left});
                if(index == 0){dis.addClass(opts.first);}
                if(index == right){dis.addClass(opts.last);}
                if(index > opts.slides-1){dis.hide();}
            });

            prvBtn.click(function(){
                if(right >= opts.slides){
                    objs.filter('.'+opts.first).removeClass(opts.first).prev().addClass(opts.first).show();
                    objs.each(function(index){
                        $(this).animate(
                            {left: '+='+cardWidth},
                            {
                                duration: 500,
                                easing: 'easeInOutQuad',
                                complete: function(){clearRight();}
                            }
                        );
                    });
                    right--;
                    if(right < opts.slides) prvBtn.addClass('inactive');
                    if(right >= opts.slides) nxtBtn.removeClass('inactive');
                }
                return false;
            });

            nxtBtn.click(function(){
                if((right + 1) < total){
                    objs.filter('.'+opts.last).removeClass(opts.last).next().addClass(opts.last).show();
                    objs.each(function(index){
                        $(this).animate(
                            {left: '-='+cardWidth},
                            {
                                duration: 500,
                                easing: 'easeInOutQuad',
                                complete: function(){clearLeft();}
                            }
                        );
                    });
                    right++;
                    if(right >= opts.slides) prvBtn.removeClass('inactive');
                    if(right+1 == total) nxtBtn.addClass('inactive');
                }
                return false;
            });
        });
    };
})(jQuery);

/* Custom mini tab switcher plugin */
;(function($){
    jQuery.fn.tabSwitcher = function(options){
        var defaults = {
            tabs : 'tabs', //tabs holder id
            content : 'tabContents', //content holder id
            active : 'active', // active tab class name
            speed : 'fast' //animation speed
        };

        return this.each(function(){

            var opts = $.extend(defaults, options); //replacing defaults with user provided options through jQuery.extend method
            var val = $('#'+ opts.tabs).find('.' + opts.active +' a').attr('href');//retrieving active tabs id

            $('>li', '#'+ opts.content).fadeOut().filter(val).fadeIn(opts.speed);//hiding all but active tabs content

            var $obj = $(this);

            $obj.find('a').click(function(){
                if(!$(this).parent().hasClass(opts.active)){ //Checking this is the vary same tab which is already active/showing
                    var $this = $(this);
                    var $new = $this.attr('href'); //retrieving its associated contents id
                    var $old = $('.'+opts.active, $obj).find('a').attr('href'); //retrieving old active tabs id
                    $($old).fadeOut(opts.speed, function(){$($new).fadeIn(opts.speed);});//first, fading out old active div and then fading in new div

                    $('>li', $obj).removeClass(opts.active);//removing active tabs class
                    $this.parent().addClass(opts.active);//attaching active tabs class
                    return false;
                }
            });
        });
    };
})(jQuery);

/* a mini plugin to help float our portfolio items meta elements on top of the thumbs. */
(function($){
    $.fn.circlePortHover = function(){
        return this.each(function(){
            $(this).find('li').each(function(){
                var elem = $(this);
                var img = elem.find('.thumb');
                var linkBtn = img.find('.link');
                var btn = img.find('.btn');
                img.find('.link').css('right', '-'+200+'px');
                img.find('.btn').css('left', '-'+200+'px');
                img.hoverIntent(function(){
                    img.find('.link').animate({'right': '5px'},{duration: 'fast'});
                    img.find('.btn').animate({'left': '5px'},{duration: 'fast'});
                    return false;
                }, function(){
                    img.find('.link').animate({'right': '-'+linkBtn.outerWidth(true)+'px'},{duration: 'fast'});
                    img.find('.btn').animate({'left': '-'+btn.outerWidth(true)+'px'},{duration: 'fast'});
                    return false;
                });
            });

        });
    };
})(jQuery);

/* jQuery.imagesLoaded Plugin */
(function(c,n){var k="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==";c.fn.imagesLoaded=function(l){function m(){var b=c(h),a=c(g);d&&(g.length?d.reject(e,b,a):d.resolve(e));c.isFunction(l)&&l.call(f,e,b,a)}function i(b,a){b.src===k||-1!==c.inArray(b,j)||(j.push(b),a?g.push(b):h.push(b),c.data(b,"imagesLoaded",{isBroken:a,src:b.src}),o&&d.notifyWith(c(b),[a,e,c(h),c(g)]),e.length===j.length&&(setTimeout(m),e.unbind(".imagesLoaded")))}var f=this,d=c.isFunction(c.Deferred)?c.Deferred():
0,o=c.isFunction(d.notify),e=f.find("img").add(f.filter("img")),j=[],h=[],g=[];e.length?e.bind("load.imagesLoaded error.imagesLoaded",function(b){i(b.target,"error"===b.type)}).each(function(b,a){var e=a.src,d=c.data(a,"imagesLoaded");if(d&&d.src===e)i(a,d.isBroken);else if(a.complete&&a.naturalWidth!==n)i(a,0===a.naturalWidth||0===a.naturalHeight);else if(a.readyState||a.complete)a.src=k,a.src=e}):m();return d?d.promise(f):f}})(jQuery);


/**
 * jQuery Masonry v2.1.03
 * A dynamic layout plugin for jQuery
 * The flip-side of CSS Floats
 * http://masonry.desandro.com
 *
 * Licensed under the MIT license.
 * Copyright 2011 David DeSandro
 */
(function(a,b,c){"use strict";var d=b.event,e;d.special.smartresize={setup:function(){b(this).bind("resize",d.special.smartresize.handler)},teardown:function(){b(this).unbind("resize",d.special.smartresize.handler)},handler:function(a,b){var c=this,d=arguments;a.type="smartresize",e&&clearTimeout(e),e=setTimeout(function(){jQuery.event.handle.apply(c,d)},b==="execAsap"?0:100)}},b.fn.smartresize=function(a){return a?this.bind("smartresize",a):this.trigger("smartresize",["execAsap"])},b.Mason=function(a,c){this.element=b(c),this._create(a),this._init()},b.Mason.settings={isResizable:!0,isAnimated:!1,animationOptions:{queue:!1,duration:500},gutterWidth:0,isRTL:!1,isFitWidth:!1,containerStyle:{position:"relative"}},b.Mason.prototype={_filterFindBricks:function(a){var b=this.options.itemSelector;return b?a.filter(b).add(a.find(b)):a},_getBricks:function(a){var b=this._filterFindBricks(a).css({position:"absolute"}).addClass("masonry-brick");return b},_create:function(c){this.options=b.extend(!0,{},b.Mason.settings,c),this.styleQueue=[];var d=this.element[0].style;this.originalStyle={height:d.height||""};var e=this.options.containerStyle;for(var f in e)this.originalStyle[f]=d[f]||"";this.element.css(e),this.horizontalDirection=this.options.isRTL?"right":"left",this.offset={x:parseInt(this.element.css("padding-"+this.horizontalDirection),10),y:parseInt(this.element.css("padding-top"),10)},this.isFluid=this.options.columnWidth&&typeof this.options.columnWidth=="function";var g=this;setTimeout(function(){g.element.addClass("masonry")},0),this.options.isResizable&&b(a).bind("smartresize.masonry",function(){g.resize()}),this.reloadItems()},_init:function(a){this._getColumns(),this._reLayout(a)},option:function(a,c){b.isPlainObject(a)&&(this.options=b.extend(!0,this.options,a))},layout:function(a,b){for(var c=0,d=a.length;c<d;c++)this._placeBrick(a[c]);var e={};e.height=Math.max.apply(Math,this.colYs);if(this.options.isFitWidth){var f=0;c=this.cols;while(--c){if(this.colYs[c]!==0)break;f++}e.width=(this.cols-f)*this.columnWidth-this.options.gutterWidth}this.styleQueue.push({$el:this.element,style:e});var g=this.isLaidOut?this.options.isAnimated?"animate":"css":"css",h=this.options.animationOptions,i;for(c=0,d=this.styleQueue.length;c<d;c++)i=this.styleQueue[c],i.$el[g](i.style,h);this.styleQueue=[],b&&b.call(a),this.isLaidOut=!0},_getColumns:function(){var a=this.options.isFitWidth?this.element.parent():this.element,b=a.width();this.columnWidth=this.isFluid?this.options.columnWidth(b):this.options.columnWidth||this.$bricks.outerWidth(!0)||b,this.columnWidth+=this.options.gutterWidth,this.cols=Math.floor((b+this.options.gutterWidth)/this.columnWidth),this.cols=Math.max(this.cols,1)},_placeBrick:function(a){var c=b(a),d,e,f,g,h;d=Math.ceil(c.outerWidth(!0)/(this.columnWidth+this.options.gutterWidth)),d=Math.min(d,this.cols);if(d===1)f=this.colYs;else{e=this.cols+1-d,f=[];for(h=0;h<e;h++)g=this.colYs.slice(h,h+d),f[h]=Math.max.apply(Math,g)}var i=Math.min.apply(Math,f),j=0;for(var k=0,l=f.length;k<l;k++)if(f[k]===i){j=k;break}var m={top:i+this.offset.y};m[this.horizontalDirection]=this.columnWidth*j+this.offset.x,this.styleQueue.push({$el:c,style:m});var n=i+c.outerHeight(!0),o=this.cols+1-l;for(k=0;k<o;k++)this.colYs[j+k]=n},resize:function(){var a=this.cols;this._getColumns(),(this.isFluid||this.cols!==a)&&this._reLayout()},_reLayout:function(a){var b=this.cols;this.colYs=[];while(b--)this.colYs.push(0);this.layout(this.$bricks,a)},reloadItems:function(){this.$bricks=this._getBricks(this.element.children())},reload:function(a){this.reloadItems(),this._init(a)},appended:function(a,b,c){if(b){this._filterFindBricks(a).css({top:this.element.height()});var d=this;setTimeout(function(){d._appended(a,c)},1)}else this._appended(a,c)},_appended:function(a,b){var c=this._getBricks(a);this.$bricks=this.$bricks.add(c),this.layout(c,b)},remove:function(a){this.$bricks=this.$bricks.not(a),a.remove()},destroy:function(){this.$bricks.removeClass("masonry-brick").each(function(){this.style.position="",this.style.top="",this.style.left=""});var c=this.element[0].style;for(var d in this.originalStyle)c[d]=this.originalStyle[d];this.element.unbind(".masonry").removeClass("masonry").removeData("masonry"),b(a).unbind(".masonry")}},b.fn.imagesLoaded=function(a){function i(a){var c=a.target;c.src!==f&&b.inArray(c,g)===-1&&(g.push(c),--e<=0&&(setTimeout(h),d.unbind(".imagesLoaded",i)))}function h(){a.call(c,d)}var c=this,d=c.find("img").add(c.filter("img")),e=d.length,f="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==",g=[];e||h(),d.bind("load.imagesLoaded error.imagesLoaded",i).each(function(){var a=this.src;this.src=f,this.src=a});return c};var f=function(b){a.console&&a.console.error(b)};b.fn.masonry=function(a){if(typeof a=="string"){var c=Array.prototype.slice.call(arguments,1);this.each(function(){var d=b.data(this,"masonry");if(!d)f("cannot call methods on masonry prior to initialization; attempted to call method '"+a+"'");else{if(!b.isFunction(d[a])||a.charAt(0)==="_"){f("no such method '"+a+"' for masonry instance");return}d[a].apply(d,c)}})}else this.each(function(){var c=b.data(this,"masonry");c?(c.option(a||{}),c._init()):b.data(this,"masonry",new b.Mason(a,this))});return this}})(window,jQuery);



/* Site Initialization JavaScript Codes */
;(function($){

    /* Adding masonry scripts to portfolio items. */
    $(document).ready(function(){
        var port2 = $('.portCol2.addMasonry');
        port2.imagesLoaded(function(){
          port2.masonry({
            itemSelector : '.mb',
            columnWidth : 510
          });
        });
        var port3 = $('.portCol3.addMasonry');
        port3.imagesLoaded(function(){
          port3.masonry({
            itemSelector : '.mb',
            columnWidth : 340
          });
        });
        var port4 = $('.portCol4.addMasonry');
        port4.imagesLoaded(function(){
          port4.masonry({
            itemSelector : '.mb',
            columnWidth : 255
          });
        });
    });

    /* scrollTo function declarations using 'scrollTo.js' jquery plugin */
    $(document).ready(function(){
        var $window = $(window);
        $('.reply').click(function(){
            $window.stop().scrollTo($('#commentForm'), 900);
        });
    });

    /* circle port hover function */
    $(document).ready(function(){
        $('.portCol3, .portCol4').circlePortHover();
    });

    /* working with form labels */
    $(document).ready(function(){
        $('#nlForm').hidingLabel();
        $('#searchForm').hidingLabel();
        $('#commentForm form').hidingLabel();
        $('#cntForm').hidingLabel();
    });

    /* Form validation */
    $(document).ready(function(){
        $('#commentForm form').tinyValidator();
        $('#cntForm').tinyValidator({ajax: true});
    });

    /* Initializing easySlider */
    $(document).ready(function(){
        $('#clients ul').easySlider({slides: 6});
        $('.featuredPorts').easySlider({slides: 4});
    });

    /* pages header image sliders for any pages */
    $(document).ready(function(){
        if ($('#imageBox').find('.image.slides').length > 0){
            $('#imageBox').find('.image.slides').find('ul').cycle({
                fx: 'fade',
                speed: 500,
                timeout: 5000,
                pause: 1,
                rev: 1,
                randomizeEffects: false,
                easing: 'easeInOutQuad', //jquery.easing library/plugin is required for this functionality
                next: '',
                prev: '',
                pager: '',
                cleartypeNoBg: true
            });
        }
    });

    /* slider for featured feedback */
    $(document).ready(function(){
        if ($('#feedback ul').length > 0){
            $('#feedback ul').cycle({
                fx: 'scrollVert',
                speed: 500,
                timeout: 5000,
                pause: 1,
                rev: 0,
                randomizeEffects: false,
                easing: 'easeInOutQuad', //jquery.easing library/plugin is required for this functionality
                next:   '#feedback .next',
                prev:   '#feedback .prev',
                pager:  '',
                cleartypeNoBg: true
            });
        }
    });

    /* portfolio post page slides */
    $(document).ready(function(){
        if ($('#portSlides ul').length > 0){
            $('#portSlides ul').cycle({
                fx: 'fade',
                speed: 500,
                timeout: 5000,
                pause: 1,
                rev: 0,
                randomizeEffects: false,
                easing: 'easeInOutQuad',
                next:   '#portSlides .next',
                prev:   '#portSlides .prev',
                pager:  '',
                cleartypeNoBg: true
            });
        }
    });

    /* sidebar feedback slides */
    $(document).ready(function(){
        if ($('#sbFeedback ul').length > 0){
            $('#sbFeedback ul').cycle({
                fx: 'fade',
                speed: 500,
                timeout: 5000,
                pause: 1,
                rev: 0,
                randomizeEffects: false,
                easing: 'easeInOutQuad',
                next:   '#sbFeedback .next',
                prev:   '#sbFeedback .prev',
                pager:  '',
                cleartypeNoBg: true
            });
        }
    });

    /* Twitter plugin for home and about pages */
//    $(document).ready(function(){
//        $("#tweets .contents").tweet({
//            username: "palpaldal",
//            join_text: "auto",
//            avatar_size: 40,
//            count: 3,
//            auto_join_text_default: "",
//            auto_join_text_ed: "",
//            auto_join_text_ing: "",
//            auto_join_text_reply: "",
//            auto_join_text_url: "",
//            loading_text: "loading tweets..."
//        });
//    });

    /* a modified/tricked initializer to initialize cycle plugins on loaded tweets */
    $('#tweets').ready(function(){
        var addCycle2Tweet = function(){
            if ($('#tweets .tweet_list').length > 0){
                $('#tweets .tweet_list').cycle({
                    fx: 'scrollVert',
                    speed: 500,
                    timeout: 5000,
                    pause: 1,
                    rev: 0,
                    randomizeEffects: false,
                    easing: 'easeInOutQuad', //jquery.easing library/plugin is required for this functionality
                    next:   '#tweets .next',
                    prev:   '#tweets .prev',
                    pager:  '',
                    cleartypeNoBg: true
                });
            }
            else{
                setTimeout(function(){addCycle2Tweet();}, 2000);
            }
        };
        if($('#tweets').length > 0){
            addCycle2Tweet();
        }
    });


    /* sidear twitter widget */
    $(document).ready(function(){
        $("#sbTweets").tweet({
            username: "palpaldal",
            join_text: "auto",
            avatar_size: 40,
            count: 3,
            auto_join_text_default: "",
            auto_join_text_ed: "",
            auto_join_text_ing: "",
            auto_join_text_reply: "",
            auto_join_text_url: "",
            loading_text: "loading tweets..."
        });
    });

    /* Initializing Tab Switcher */
    $(document).ready(function(){
        if($('#tabs').length > 0){
            $('#tKeys').tabSwitcher({tabs: 'tKeys', content: 'tConts'});
        }
    });


    /*
    *   prettyPhoto startup function declarations using 'prettyPhoto.js' jquery plugin
    *   These short codes'll add a little dark effect on hover and also an appropriate icon for that particular content.
    *   You don't need to do anything here, just leave it as it is.
    */
    $(document).ready(function(){
        if($.fn.prettyPhoto){
            $("a[rel^='prettyPhoto']").each(function(index){
                var imgHTML = $('<span class="prettyItemHover img"></span>');
                var indocHTML = $('<span class="prettyItemHover indoc"></span>');
                var movHTML = $('<span class="prettyItemHover mov"></span>');
                var flashHTML = $('<span class="prettyItemHover flash"></span>');
                var ele = $(this);
                var itemSrc = ele.attr('href');
                ele.css({'position': 'relative', 'display': 'block'});
                if(itemSrc.match(/youtube\.com\/watch/i) || itemSrc.match(/vimeo\.com/i) || itemSrc.indexOf('.mov') != -1){
                    ele.append(movHTML);
                }
                else if(itemSrc.indexOf('iframe') != -1 || itemSrc.substr(0,1) == '#'){
                    ele.append(indocHTML);
                }
                else if(itemSrc.indexOf('.swf') != -1){
                    ele.append(flashHTML);
                }
                else{
                    ele.append(imgHTML);
                }
            })
            .hoverIntent(function(){
                $(this).children('.prettyItemHover').fadeIn('fast');
                return;
            }, function(){
                $(this).children('.prettyItemHover').fadeOut('fast');
                return;
            })
            .prettyPhoto();
        }
    });

    /* jQuery quicksand plugin */
    $(document).ready(function(){
        var read_button = function (class_names) {
                var r = {
                    selected: false,
                    type: 0
                };
                for (var i = 0; i < class_names.length; i++) {
                    if (class_names[i].indexOf('selected-') == 0) {
                        r.selected = true;
                    }
                    if (class_names[i].indexOf('segment-') == 0) {
                        r.segment = class_names[i].split('-')[1];
                    }
                };
                return r;
            };
        var determine_kind = function ($buttons) {
                var $selected = $buttons.parent().filter('[class*="selected-"]');
                return $selected.find('a').attr('data-value');
            };
        var $preferences = {
            duration: 800,
            useScaling: true,
            easing: 'easeInOutQuad',
            adjustHeight: 'dynamic'
        };

        var $list = $('.qsList');
        var $data = $list.clone();

        var $controls = $('.qsKeys');

        $controls.each(function (i){
            var $control = $(this);
            var $buttons = $control.find('a');
            $buttons.click(function (e) {
                var $button = $(this);
                var $button_container = $button.parent();
                var button_properties = read_button($button_container.attr('class').split(' '));
                var selected = button_properties.selected;
                var button_segment = button_properties.segment;
                if (!selected) {
                    for(var i = 0; i < $buttons.length; i++){
                        $buttons.parent().removeClass('selected-'+i);
                    }
                    $button_container.addClass('selected-' + button_segment);
                    var sorting_kind = determine_kind($controls.find('a'));
                    if (sorting_kind == 'all') {
                        var $filtered_data = $data.find('>li');
                    } else {
                        var $filtered_data = $data.find('>li.' + sorting_kind);
                    }
                    $list.quicksand($filtered_data, $preferences,
                    function(){
                        if($.fn.prettyPhoto){
                            $("a[rel^='prettyPhoto']").each(function(index){
                                var imgHTML = $('<span class="prettyItemHover img"></span>');
                                var indocHTML = $('<span class="prettyItemHover indoc"></span>');
                                var movHTML = $('<span class="prettyItemHover mov"></span>');
                                var flashHTML = $('<span class="prettyItemHover flash"></span>');
                                var ele = $(this);
                                var itemSrc = ele.attr('href');
                                ele.css({'position': 'relative', 'display': 'block'});
                                if(itemSrc.match(/youtube\.com\/watch/i) || itemSrc.match(/vimeo\.com/i) || itemSrc.indexOf('.mov') != -1){
                                    ele.append(movHTML);
                                }
                                else if(itemSrc.indexOf('iframe') != -1 || itemSrc.substr(0,1) == '#'){
                                    ele.append(indocHTML);
                                }
                                else if(itemSrc.indexOf('.swf') != -1){
                                    ele.append(flashHTML);
                                }
                                else{
                                    ele.append(imgHTML);
                                }
                            })
                            .hoverIntent(function(){
                                $(this).children('.prettyItemHover').fadeIn('fast');
                                return false;
                            }, function(){
                                $(this).children('.prettyItemHover').fadeOut('fast');
                                return false;
                            })
                            .prettyPhoto();
                        }
                        if($.fn.circlePortHover){
                            $('.portCol3, .portCol4').circlePortHover();
                        }
                    });
                }
                e.preventDefault();
            });
        });
    });
})(jQuery);

/* Patterns */
$(document).ready(function(){
    $('#contentPatterns').find('li').each(function(){
        var elem = $(this).find('a');
        elem.click(function(){
            var pattClass = elem.attr('class');
            if(pattClass == 'default'){
                $('body').removeAttr('style');
            }
            else{
            $('body').css('background-image', 'url(files/images/patterns/light/'+pattClass+'.png');
            }
            return false;
        });
    });

    var headerColor = 'light';
    /* resetting dark and light for header */
    $(document).ready(function(){
        var removeActiveClass = function(){
            $('#headerBGColor').find('li').find('a').removeClass('active');
        };
        $('#headerBGColor').find('li').each(function(){
            var colorLink = $(this).find('a');
            colorLink.click(function(){
                if(!colorLink.hasClass('active')){
                    headerColor = colorLink.attr('data-mode');
                    if(colorLink.attr('data-mode') == 'light'){
                        $('#imageBox').css({'background-color': '#fff', 'background-image': 'url(files/images/noise-patt.png)'});
                        $('#headerPatterns').find('li[data-type=light]').show();
                        $('#headerPatterns').find('li[data-type=dark]').hide();
                    }
                    else{
                        $('#imageBox').css({'background-color': '#222', 'background-image': 'url(files/images/noise-patt-dark.png)'});
                        $('#headerPatterns').find('li[data-type=light]').hide();
                        $('#headerPatterns').find('li[data-type=dark]').show();
                    }
                    removeActiveClass();
                    colorLink.addClass('active');
                }
                return false;
            });
        });
    });

    /* changing header patterns */
    $('#headerPatterns').find('li').each(function(){
        var type = $(this).attr('data-type');
        if(type == 'light'){
            var elem = $(this).find('a');
            elem.click(function(){
                var pattClass = elem.attr('class');
                if(pattClass == 'default'){
                    $('#imageBox').css('background-image', 'url(files/images/noise-patt.png');
                }
                else{
                    $('#imageBox').css('background-image', 'url(files/images/patterns/light/'+pattClass+'.png');
                }
                return false;
            });
        }
        else{
            var elem = $(this).find('a');
            elem.click(function(){
                var pattClass = elem.attr('class');
                if(pattClass == 'default'){
                    $('#imageBox').css('background-image', 'url(files/images/noise-patt-dark.png');
                }
                else{
                    $('#imageBox').css('background-image', 'url(files/images/patterns/dark/'+pattClass+'.png');
                }
                return false;
            });
        }

    });

    $('#footerPatterns').find('li').each(function(){
        var elem = $(this).find('a');
        elem.click(function(){
            var pattClass = elem.attr('class');
            if(pattClass == 'default'){
                $('#footer').removeAttr('style');
                $('#footer').find('.stHead').find('h2').removeAttr('style');
                $('#secondary').find('.static').removeAttr('style');
                $('#secondary').find('#tConts').removeAttr('style');
                $('#secondary').find('.dynamic').removeAttr('style');
                $('#secondary').find('.stHead').find('h2').removeAttr('style');
            }
            else{
                $('#footer').css('background-image', 'url(files/images/patterns/dark/'+pattClass+'.png');
                $('#footer').find('.stHead').find('h2').css('background-image', 'url(files/images/patterns/dark/'+pattClass+'.png');
                $('#secondary').find('.static').css('background-image', 'url(files/images/patterns/dark/'+pattClass+'.png');
                $('#secondary').find('#tConts').css('background-image', 'url(files/images/patterns/dark/'+pattClass+'.png');
                $('#secondary').find('.dynamic').css('background-image', 'url(files/images/patterns/dark/'+pattClass+'.png');
                $('#secondary').find('.stHead').find('h2').css('background-image', 'url(files/images/patterns/dark/'+pattClass+'.png');
            }
            return false;
        });
    });

});


$(document).ready(function(){
    var lColor = function(){
        var cls = (Cookie.get('rstarLink')) ? Cookie.get('rstarLink') : 'default';
        $('#colors').attr('href', '/files/codes/css/colors/'+cls+'.css');
        $('.'+cls, '#themeColors').parent().addClass('active').siblings().removeClass('active');
    };

    lColor();

    $('a', '#themeColors').click(function(){
        var lnk = $(this);
        Cookie.set("rstarLink", lnk.attr('class'));
        lColor();
        return false;
    });
});

Cookie = {
    set: function(key, value, minstoexpire){
        var expires = "";
        if(minstoexpire){
            var date = new Date();
            date.setTime(date.getTime()+(minstoexpire*60*1000));
            expires = "; expires="+date.toGMTString();
        }
        document.cookie = encodeURIComponent(key)+"="+encodeURIComponent(value)+expires+"; path=/";
        return value;
    },

    get: function(key){
        var nameCompare = key + "=";
        var cookieArr = document.cookie.split(';');
        for(var i = 0; i < cookieArr.length; i++){
            var aCrumb = cookieArr[i].split("=");
            var currentKey = decodeURIComponent(aCrumb[0]);
            if(key == currentKey || " " + key == currentKey){
                return decodeURIComponent(aCrumb[1]);
            }
        }
        return null;
    }
};

