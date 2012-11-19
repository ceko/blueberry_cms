(($, window) ->

	class MenuWidget		
		constructor: (@$invoking_element, @menuitems) ->
					
		show: (event) ->
			#Hide all other open menus			
			event.stopPropagation()
			if !@$menu_element
				html = "<div class='berry_menu_widget'>"
				html += "<div class='berry_menu_widgetitem close_menu'>cancel</div>"
				for option in @menuitems				
					html += "<div class='berry_menu_widgetitem #{option.label}'>#{option.label}</div>"
				html += "</div>"			
				@$menu_element = $(html)
				@$menu_element.find(".close_menu").click =>
					@$menu_element.hide()
				for option in @menuitems
					@$menu_element.find(".#{option.label}")
						.click(option.callback)						
				@$menu_element.find('.berry_menu_widgetitem')
					.mouseover ->
						$(this).addClass('hover')
					.mouseout ->
						$(this).removeClass('hover')				
				$('body').append(@$menu_element)
				$('html').click =>
					@$menu_element.hide()			
			
			@$menu_element.css({
				position:'absolute',
				top:event.pageY,
				left:event.pageX,
			})
			@$menu_element.show()
			
		@hide_all: ->
			$('.berry_menu_widget').hide()		   

	class MenuWidgetItem	
		constructor: (@label, @callback)->

	window.bb_cms or= {}
	window.bb_cms.MenuWidget = MenuWidget
	window.bb_cms.MenuWidgetItem = MenuWidgetItem	
		
)(jQuery, window)		