(($, window) ->

	class BerryPanel
		@hover_class = 'hover'
		@add_block_class = 'berry_add_block'
			
		constructor: (@$element) ->
			@blocks = []
			@$element.find('.berry_edit_block').each (idx, el) =>
				@blocks.push(new BerryBlock($(el)));
			
			@._attach_listeners()
				
		_attach_listeners: ->
			@$element
				.mouseover =>
					@$element.addClass(BerryPanel.hover_class)
				.mouseout =>
					@$element.removeClass(BerryPanel.hover_class)
			
			@$element.find(".#{BerryPanel.add_block_class}").colorbox(window.bb_cms.colorbox_defaults)
	
	class BerryBlock
		@hover_class = 'hover'
			
		constructor: (@$element) ->	
			@._attach_listeners()
			@id = @$element.attr('block_id');
		
		show_menu: (event) ->
			if !@clickmenu 				
				editoption = new window.bb_cms.MenuWidgetItem("edit", @._edit)
				deleteoption = new window.bb_cms.MenuWidgetItem("delete", @._delete)
				@clickmenu = new window.bb_cms.MenuWidget(@$element, [editoption, deleteoption])
			
			window.bb_cms.MenuWidget.hide_all()
			@clickmenu.show(event)						
			
		_edit: =>			
			colorbox_settings = window.bb_cms.colorbox_defaults
			colorbox_settings['href'] = "edit-block/#{@id}" 
			$.colorbox(window.bb_cms.colorbox_defaults)
		
		_delete: =>
			if confirm("Are you sure?")
				window.location = window.location + "delete-block/#{@id}"
		
		_attach_listeners: ->
			@$element
				.mouseover =>
					@$element.addClass(BerryBlock.hover_class)
				.mouseout =>
					@$element.removeClass(BerryBlock.hover_class)		
				.click (event) =>
					@.show_menu(event)					
	
	#Initialization, keep near the bottom.
	$ ->
		$('.berry_edit_panel').each (idx, el) ->
			el.BerryPanel = new BerryPanel($(this))
			
	
	window.bb_cms or= {}
	window.bb_cms.BerryPanel = BerryPanel
	window.bb_cms.BerryBlock = BerryBlock
	window.bb_cms.colorbox_defaults = {
		iframe : true, 
		width: "300px", 
		height: "400px"
	} 
		
)(jQuery, window)		
			
		
	