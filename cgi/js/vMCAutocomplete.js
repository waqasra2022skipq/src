$.widget('custom.mcautocomplete', $.ui.autocomplete, {
  _create: function () {
    this._super();
    this.widget().menu("option", "items", "> :not(.ui-widget-header)");
  },
  _renderMenu: function (ul, items) {
    var self = this,
      thead;
    if (this.options.showHeader) {
      tr = $('<tr></tr>');
      $.each(this.options.columns, function (index, item) {
        tr.append('<th style="width:' + item.width + ';">' + item.name + '</th>');
      });
      ul.append(tr);
    }
    $.each(items, function (index, item) {
      self._renderItem(ul, item);
    });
  },
  _renderItem: function (ul, item) {
    var t = '',
      result = '';
    $.each(this.options.columns, (index, column) => {
      var whole_word = item[column.valueField ? column.valueField : index];
      var current_search_string = this.element.val();

      // Highlight current search term.
      var regex;
      if (current_search_string !== '*') {
        regex = new RegExp( '(' + 
          current_search_string + ')', 'gi' );
        if (whole_word !== null && whole_word !== undefined) {
          whole_word = whole_word.replace(
            regex, "<b>$1</b>" );
        }
      }

      t += '<td style="width:'+ column.width +';">' + whole_word + '</td>';
    });

    result = $('<tr></tr>')
      .data('ui-autocomplete-item', item)
      .append(t)
      .appendTo(ul);
    return result;
  }
});
