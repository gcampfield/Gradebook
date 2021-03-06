var class_template, category_template;

function flash(message) { //*TODO
  console.log(message);
}

function clean(number) {
  if ((number + '').search(/\./) == -1) {
    return number + '.0';
  }
  return number + '';
}

function make_total(points, total) {
  var text;
  if (total > 0) {
    text = '<p class="total"><b>Total:</b> POINTS/TOTAL = PERCENT%</p>';
    text = text.replace('PERCENT', (points/total*100).toFixed(2));
  } else {
    text = '<p class="total"><b>Total:</b> POINTS/TOTAL</p>'
  }
  text = text.replace('POINTS', points);
  text = text.replace('TOTAL', total);
  return text;
}

function make_total_class(points, total, grade) {
  var text;
  if (total > 0) {
    text = '<p class="total"><b>Total:</b> POINTS/TOTAL = PERCENT% | GRADE</p>';
    text = text.replace('PERCENT', (points/total*100).toFixed(2));
  } else {
    text = '<p class="total"><b>Total:</b> POINTS/TOTAL | GRADE</p>'
  }
  text = text.replace('POINTS', points);
  text = text.replace('TOTAL', total);
  text = text.replace('GRADE', grade);
  return text;
}

function add_class(e) {
  var form = $(this);
  $.post(window.location.origin + '/grades/new/class/', form.serialize(),
    function (data) {
      if (data.error) {
        flash(data.error);
      } else {
        var new_class = $('<div/>').html(class_template).contents();
        new_class.find('h3 a').attr('href', '/grades/' + data.class_.id + '/');
        new_class.find('h3 a').text(data.class_.name);
        new_class.find('.delete-class').attr('id', data.class_.id);
        new_class.find('input[name="class"]').val(data.class_.id);
        new_class.find('.total').html(make_total_class(data.class_.points,
                                                       data.class_.total,
                                                       data.class_.grade));
        new_class.insertBefore(form);
        $('.add-category').submit(add_category);
        $('.delete-class').click(delete_class);
      }
    }
  );

  form.children('input[type="text"]').val('');
  return false;
}

function add_category(e) {
  var form = $(this);
  $.post(window.location.origin + '/grades/new/category/', form.serialize(),
    function (data) {
      if (data.error) {
        flash(data.error);
      } else {
        var new_category = $('<div/>').html(category_template).contents();
        new_category.find('h4').text(data.category.name);
        new_category.find('.delete-category').attr('id', data.category.id);
        new_category.find('input[name="category"]').val(data.category.id);
        new_category.insertBefore(form);
        $('.add-grade').submit(add_grade);
        $('.delete-category').click(delete_category);
      }
    }
  );

  form.children('input[type="text"]').val('');
  return false;
}

function add_grade(e) {
  var form = $(this),
      category = form.parent(),
      class_ = category.parent();
  $.post(window.location.origin + '/grades/new/grade/', form.serialize(),
    function (data) {
      if (data.error) {
        flash(data.error);
      } else {
        var new_grade = $('<p></p>');
        var text = data.grade.name ? data.grade.name + " | " : "";
        text += clean(data.grade.score) + "/" + clean(data.grade.total);
        text += '<button class="delete-grade" id="'
        text += data.grade.id
        text += '">Delete</button>';
        new_grade.html(text);
        new_grade.insertBefore(form);
        $('.delete-grade').click(delete_grade);

        if (data.grade.category_total > 0) {
          var total = make_total(data.grade.category_points,
                                 data.grade.category_total);
          if (category.find('.total').length > 0) {
            category.find('.total').html(total);
          } else {
            category.append($(total));
          }
        }

        class_.find('.total').last().html(
          make_total_class(data.grade.class_points,
                           data.grade.class_total,
                           data.grade.class_grade));
      }
    }
  );

  form.children('input[type="text"]').val('');
  return false;
}

function delete_class() {
  var button = $(this);
  $.post(window.location.origin + '/grades/delete/class/',
    {'class': button.attr('id')}, function (data) {
      if (data.error) {
        flash(data.error);
      } else {
        button.parent().remove();
      }
    }
  );
}

function delete_category() {
  var button = $(this);
  var class_ = button.parent().parent();
  $.post(window.location.origin + '/grades/delete/category/',
    {'category': button.attr('id')}, function (data) {
      if (data.error) {
        flash(data.error);
      } else {
        button.parent().remove();
        class_.find('.total').last().html(
          make_total_class(data.class_.points,
                           data.class_.total,
                           data.class_.grade));
      }
    }
  );
}

function delete_grade() {
  var button = $(this);
  var category = button.parent().parent();
  $.post(window.location.origin + '/grades/delete/grade/',
    {'grade': button.attr('id')}, function (data) {
      if (data.error) {
        flash(data.error);
      } else {
        button.parent().remove();
        if (data.category.total > 0) {
          var total = make_total(data.category.points, data.category.total);
          category.find('.total').html(total);
        } else {
          category.find('.total').remove();
        }
      }
    }
  );
}

$(document).ready(function () {
  class_template = $('template.class').html();
  category_template = $('template.category').html();

  $('.add-class').submit(add_class);
  $('.add-category').submit(add_category);
  $('.add-grade').submit(add_grade);

  $('.delete-class').click(delete_class);
  $('.delete-category').click(delete_category);
  $('.delete-grade').click(delete_grade);
});
