// Generated by CoffeeScript 1.4.0
(function() {

  (function($, window) {
    var MenuWidget, MenuWidgetItem;
    MenuWidget = (function() {

      function MenuWidget($invoking_element, menuitems) {
        this.$invoking_element = $invoking_element;
        this.menuitems = menuitems;
      }

      MenuWidget.prototype.show = function(event) {
        var html, option, _i, _j, _len, _len1, _ref, _ref1,
          _this = this;
        event.stopPropagation();
        if (!this.$menu_element) {
          html = "<div class='berry_menu_widget'>";
          html += "<div class='berry_menu_widgetitem close_menu'>cancel</div>";
          _ref = this.menuitems;
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            option = _ref[_i];
            html += "<div class='berry_menu_widgetitem " + option.label + "'>" + option.label + "</div>";
          }
          html += "</div>";
          this.$menu_element = $(html);
          this.$menu_element.find(".close_menu").click(function() {
            return _this.$menu_element.hide();
          });
          _ref1 = this.menuitems;
          for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
            option = _ref1[_j];
            this.$menu_element.find("." + option.label).click(option.callback);
          }
          this.$menu_element.find('.berry_menu_widgetitem').mouseover(function() {
            return $(this).addClass('hover');
          }).mouseout(function() {
            return $(this).removeClass('hover');
          });
          $('body').append(this.$menu_element);
          $('html').click(function() {
            return _this.$menu_element.hide();
          });
        }
        this.$menu_element.css({
          position: 'absolute',
          top: event.pageY,
          left: event.pageX
        });
        return this.$menu_element.show();
      };

      MenuWidget.hide_all = function() {
        return $('.berry_menu_widget').hide();
      };

      return MenuWidget;

    })();
    MenuWidgetItem = (function() {

      function MenuWidgetItem(label, callback) {
        this.label = label;
        this.callback = callback;
      }

      return MenuWidgetItem;

    })();
    window.bb_cms || (window.bb_cms = {});
    window.bb_cms.MenuWidget = MenuWidget;
    return window.bb_cms.MenuWidgetItem = MenuWidgetItem;
  })(jQuery, window);

}).call(this);
