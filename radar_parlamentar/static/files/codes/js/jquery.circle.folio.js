/*
Extending JS Array features
to return the max/min value from
an array instead of one of two values.
*/
Array.max = function(array){
	return Math.max.apply(Math, array);
};

Array.min = function(array){
	return Math.min.apply(Math, array);
};

;(function($){
	$.fn.circleFolio = function(options){
		var o = {
			rows : 2,
			cols : 2,
			listType : 'list',
			itemType : 'all',
			gridClass : 'portCol4',
			listClass : 'portCol2',
			pager : '#portCntrls .portPager',
			pagerBtm : '#btmPortCntrls .portPager',
			sortKeys : '#sortKeys li',
			dtCntrls : '#portCntrls .portDT'
		};
		
		$.extend(o, options);
		
		return this.each(function(){
			//directly linking to 'o'
			var rows = o.rows;
			var cols = o.cols;
			var listType = o.listType;
			var itemType = o.itemType;
			var gridClass = o.gridClass;
			var listClass = o.listClass;
			//Folio Items (Objects)
			var ports = $(this);
			var items = ports.find('>li');
			var activeItems = items;
			var totalItems = items.size();
			//Folio Items after math/props
			var oneStack = rows * cols;
			var itemWidth = activeItems.outerWidth(true);
			var stacks = Math.ceil(totalItems / oneStack);
			var cntWidth = ports.outerWidth();
			var curStack = 1;
			var contLeft = [0, 0, 0, 0];
			var contTop = [0, 0, 0, 0];
			//Controlls
			var pager = $(o.pager);
			var pagerBtm = $(o.pagerBtm);
			var sortKeys = $(o.sortKeys);
			var dtCntrls = $(o.dtCntrls);
			//others
			var dtCount = 0;
			var cntrHeight = 0;

			//This function requires many functions action before working
			var pos = function(){
				items.each(function(i){
					var elem = $(this);
					/* positioning items left */
					if(i < oneStack){/* means this is the first stack */
						elem.css('left', (itemWidth * (i%cols))+'px');
					}
					else{/* take care other stacks */
						var pad = (itemWidth * cols) * (Math.floor(i / oneStack));
						elem.css('left', ((itemWidth * (i%cols)) + pad) +'px');
					}
					/* reset the content top property to zero for new stacks */
					if(i % oneStack == 0){
						for(var i = 0; i < contTop.length; i++){
							contTop[i] = 0;
						}
					}
					/* positioning items top */
					if(i < cols){
						elem.css('top', '0px');
						contTop[i] = elem.outerHeight(true);
					}
					else if(i >= cols){
						var et = i % cols;
						elem.css('top', contTop[et]+'px');
						contTop[et] += elem.outerHeight(true);
					}
					elem.fadeIn('fast');
				});
				activeItems = items;
			};
			
			var getCntrHeight = function(){
				var height = new Array(cols);
				for(var i = 0; i < oneStack; i++){//will run for four times
					var h = activeItems.eq(((curStack - 1) * oneStack) + i).outerHeight(true);
					if(i < cols){
						height[i] = h;
					}
					else{
						height[i % cols] += h;
					}
				}
				return Array.max(height);
			}

			var setCntrHeight = function(){
				var height = getCntrHeight();
				if(cntrHeight < height){
					var h = height - cntrHeight;
					ports.animate(
						{height: '+='+h+'px'},
						{duration: 'slow'}
					)
				}
				else if(cntrHeight > height){
					var h = cntrHeight - height;
					ports.animate(
						{height: '-='+h+'px'},
						{duration: 'slow'}
					)
				}
				cntrHeight = height;
			};

			var pagerNext = function(){
				if(curStack < stacks){
					activeItems.each(function(){
						var elem = $(this);
						elem.animate(
							{left: '-='+cntWidth+'px'},
							{
								duration: 'slow'
							}
						);
					});
					curStack++;
					resetNP();//reset next/prev
					setCntrHeight();
				}
			};
			
			var pagerPrev = function(){
				if(curStack > 1){
					activeItems.each(function(){
						var elem = $(this);
						elem.animate(
							{left: '+='+cntWidth+'px'},
							{
								duration: 'slow'
							}
						);
					});
					curStack--;
					resetNP();//reset next/prev
					setCntrHeight();
				}
			};
		
			var _dtGrid = function(){
				if(dtCount == activeItems.length){
					dtCount = 0;
					ports.removeClass(listClass).addClass(gridClass);
					cols = 4;
					listType = 'grid';
					ports.find('>li').each(function(){
						var elem = $(this);
						elem.find('p').addClass('invisible');
						elem.find('.btn').appendTo(elem.find('.thumb'));
						elem.find('.meta').find('.link a').unwrap('li').addClass('link').appendTo(elem.find('.thumb'));
					});
					setItems();
					dispReset();
					hvrItems();
				}
				return;
			};
		
			var _dtList = function(){
				if(dtCount == activeItems.length){
					dtCount = 0;
					ports.removeClass(gridClass).addClass(listClass);
					cols = 2;
					listType = 'list';
					ports.find('>li').each(function(){
						var elem = $(this);
						elem.find('p').removeClass('invisible');
						elem.find('.thumb').find('.btn').appendTo(elem);
						elem.find('.thumb').find('.link').removeClass('link').appendTo(elem.find('.meta')).wrap('<li class="link">');
					});
					setItems();
					dispReset();
				}
				return;
			};
			
			var hvrItems = function(){
				items.each(function(){
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
			};
		
			var setItems = function(){
				if(itemType == 'all'){
					items = ports.find('>li');
				}
				else{
					items = ports.find('>li[data-type~='+itemType+']');
				}
				totalItems = items.length;
			};
		
			/* reset after changing disp type */
			var dispReset = function(){
				var newOneStack = cols * rows;
				itemWidth = items.outerWidth(true);
				if(newOneStack < oneStack){
					if(curStack > 1){
						//I've to decide which one should I show?
						var inViewed = ((curStack * oneStack) - oneStack);
						var newCurStack = Math.ceil((inViewed + newOneStack) / newOneStack);
						_dsOtherStacks(newOneStack, newCurStack);
					}
					else{
						_dsFirstStack(newOneStack);
					}
				}
				//then the new one is more capable
				else if(newOneStack > oneStack){
					var viewed = oneStack * curStack;//suppose = 12
					if(viewed > newOneStack){
						var newCurStack = Math.ceil(viewed / newOneStack);
						_dsOtherStacks(newOneStack, newCurStack);
					}
					else{
						_dsFirstStack(newOneStack);
					}
				}
				//add or remove 'next'/'prev' buttons 'active' class
				resetNP();
				setCntrHeight();
			};
			
			var _dsFirstStack = function(one){
				oneStack = one;
				curStack = 1;
				stacks = Math.ceil(totalItems / oneStack);
				pos();
			};
			
			var _dsOtherStacks = function(one, cur){
				oneStack = one;
				curStack = cur;
				stacks = Math.ceil(totalItems / oneStack);
				pos();
				//position each items to the left based on curStack
				activeItems.css('left', '-='+(cntWidth * (curStack - 1))+ 'px');
			};
		
			var _sort = function(){
				if(dtCount == activeItems.length){
					dtCount = 0;
					if(itemType == 'all'){
						curStack = 1;
						stacks = Math.ceil(totalItems / oneStack);
						pos();
						resetNP();//setting next/prev controlls
					}
					//otherwise take care of particular type
					else{
						reshuffle();
					}
					setCntrHeight();
				}
				return;
			};
			
			var reshuffle = function(){
				oneStack = cols * rows;
				itemWidth = items.outerWidth(true);
				curStack = 1;
				stacks = Math.ceil(totalItems / oneStack);
				pos();
				//setting the todo's
				resetNP();//setting next/prev controlls
			};
		
			var resetNP = function(){
				if(stacks == 1 || curStack == stacks){
					pager.find('.next').addClass('inactive');
					pagerBtm.find('.next').addClass('inactive');
				}
				else{
					pager.find('.next').removeClass('inactive');
					pagerBtm.find('.next').removeClass('inactive');
				}
				if(curStack == 1 || stacks == 1){
					pager.find('.prev').addClass('inactive');
					pagerBtm.find('.prev').addClass('inactive');
				}
				else{
					pager.find('.prev').removeClass('inactive');
					pagerBtm.find('.prev').removeClass('inactive');
				}
			};
		
			pager.find('.next').click(function(){
				pagerNext();
				return false;
			});

			pagerBtm.find('.next').click(function(){
				pagerNext();
				return false;
			});

		
			pager.find('.prev').click(function(){
				pagerPrev();
				return false;
			});

			pagerBtm.find('.prev').click(function(){
				pagerPrev();
				return false;
			});

			/* display type = grid */
			dtCntrls.find('.grid').click(function(){
				if(listType == 'list'){
					dtCntrls.find('.list').removeClass('active');
					$(this).addClass('active');
					activeItems.each(function(i){
						$(this).fadeOut('fast', function(){dtCount++; _dtGrid();});
					});
				}
				return false;
			});

			/* display type = list */
			dtCntrls.find('.list').click(function(){
				if(listType == 'grid'){
					dtCntrls.find('.grid').removeClass('active');
					$(this).addClass('active');
					activeItems.each(function(i){
						$(this).fadeOut('fast', function(){dtCount++; _dtList();});
					});
				}
				return false;
			});

			sortKeys.each(function(){
				var key = $(this);
				key.click(function(){
					sortKeys.removeClass('active');
					key.addClass('active');
					var type = key.attr('data-key');
					if(itemType != type){
						itemType = type;
						setItems();
						activeItems.each(function(i){
							$(this).fadeOut('fast', function(){dtCount++; _sort();});
						});
						//if the key to show all
					}
					return false;
				});
			});
		
			//A self-invoked function to initiate the plugin working procedure and dependencies.
			(function(){
				items.css('position', 'absolute');
				ports.css({'overflow': 'hidden', 'position': 'relative'});
				pos();
				cntrHeight = getCntrHeight();
				ports.height(cntrHeight);
				hvrItems();
			})();

		});
	};
})(jQuery);



/* initializing */
$(document).ready(function(){
	$('#port').circleFolio({rows: 3});
});