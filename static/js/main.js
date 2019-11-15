/* Mobile Nav */
  var changedColumIds = [];
  var disableClass = 'grey lighten-5 grey-text text-lighten-1';

  $(document).ready(function(){
    updateBeforeLoading();
    toDisable();
    loadInlinePages();
    //Display shape select field in nn parameter
    $("#id_parameterCNN_Shape").css({"display":"block"})
    //Hide team select field in add machine step1
    $("#id_team").css({"display":"none"})

    $('.sidenav').sidenav();
    $('.collapsible').collapsible();
    $('.collapsible.expandable').collapsible({
      accordion: false
    });
    $('.modal').modal();
    $('.dropdown-trigger').dropdown();
    $('.tabs').tabs();

    //$('.form-machine-add ul li').find('span').eq(0).text('Select Team!!');
    $('.form-machine-add .bf-team-selected-list').find('option').eq(0).text('Select Team');
    $('select').formSelect();
    $('table[bf-data-datatable="yes"]').DataTable({
      language: {
        searchPlaceholder: "Search"
      },
    });

    /* Our codes */
    contentWidth();

    $('#modalSubmit').on('submit',function(event){
      event.preventDefault();
      alert('A');
      return false;
    });


    $('.i-reply').click(function(e){
      thisIndex = $(this).index('.i-reply')
      userID = $('.i-message-received tbody tr').eq(thisIndex).find('span').attr('data-user-id');
      userName = $('.i-message-received tbody tr').eq(thisIndex).find('span').attr('data-name');
      console.log(userName);
      $('.i-send-username').text(userName);
      $('.i-reply-area ').removeClass('hide')
      return false;
    });

    $('.i-project-is-public').click(function(){
      isChecked = $('input[name=is_public]').prop('checked');
      console.log(isChecked);

      if(isChecked){
        $('.i-machine-option-list').show();
      }else{
        $('.i-machine-option-list').hide();
        $('.i-machine-option-list input').prop('checked',false);
      }

    });

    $('body').on('keyup keypress', function(e) {
      var keyCode = e.keyCode || e.which;
      if (keyCode === 13) { 
        e.preventDefault();
        return false;
      }
    });

    $("table .click-row").on('click', function () {
      window.location = $(this).attr('line-url');
    });

    $('.i-machine-option-list input').on('click',function(){
      clickedSelection = $('.i-machine-option-list input').index(this);
      $('.i-machine-option-list input').prop('checked',false);
      $('.i-machine-option-list input').eq(clickedSelection).prop('checked',true);
    });

    $('.new-consulting-request label input').on('click',function(){
      clickedSelection = $('.new-consulting-request label input').index(this);
      $('.new-consulting-request label input').prop('checked',false);
      $('.new-consulting-request label input').eq(clickedSelection).prop('checked',true);

      if( clickedSelection == 1 ){
        $('.related_machine').removeClass('hide');
      }else{
        $('.related_machine').addClass('hide');
      }

    });

    $('#new-consulting-request-form').on('submit',function(){
      $('.machine-alert').addClass('hide');
      $('.existing-alert').addClass('hide');

      if( $('.new-consulting-request label input').eq(1).prop('checked') && $('#id_related_machine').val() == '' )
      {
        $('.existing-alert').removeClass('hide');
        return false;
      }else if( !$('.new-consulting-request label input').eq(0).prop('checked') && !$('.new-consulting-request label input').eq(1).prop('checked') ){
        $('.machine-alert').removeClass('hide');
        return false;
      }
    });

    $('input[name="i-is-agree"]').on('change',function(){
      $('a[name="i-next-after-agree"]').attr('disabled',!$(this).prop('checked'));
    });

    $('input[name="chose-machine"]').on('change',function(){
      selectedID = $(this).attr('id');
      selectedID == 'existingMachine' ? $('.available-machines').removeClass('hide') :  $('.available-machines').addClass('hide') ;
    });

    $('#createTeam').on('click', function(){
      alert('AAAAA');
    });

    $(window).resize(function(){
      contentWidth();
    });

    $('.bf-sub-menu').mouseenter(function(){
      bfTop = $('.bf-sub-menu-start').position().top + $(document).find(this).position().top;
      bfLeft = $(document).find(this).position().left + $(this).outerWidth();
      $(this).find('div')
        .css('top',bfTop+'px')
        .css('left',bfLeft+'px')
        .show();

    });
    $('.bf-sub-menu').mouseleave(function(){
      $('.submenu').hide();
    });
   

    // Description Change
    $('table[name="bf-on-off-table"] textarea').on('change',function(){
      var elem = $(this);
      var elementIndex = $('table[name="bf-on-off-table"] textarea').index(elem);
      saveColumn(elementIndex);
    });

    // Description Keyboard Pressing
    $('table[name="bf-on-off-table"] textarea').on('keyup',function(){
      bottomButton('Save','green');
    });

    // Input/Output Change
    $('table[name="bf-on-off-table"] .ioLine').on('change',function(){
      bottomButton('Save','green');
      var elem = $(this);
      var elementIndex = $('table[name="bf-on-off-table"] .ioLine').index(elem);
      saveColumn(elementIndex);
   });
   
   // On/Off Change
    $('.bf-on-off-machine').on('change',function(){
      bottomButton('Save','green');
      var elem = $(this);
      var elementIndex = $('.bf-on-off-machine').index(elem);
      var columnIndex = elementIndex + 1 ;
      saveColumn(elementIndex);
      
      if(elem.prop('checked')){
        $('table[name=bf-on-off-table] th').eq(elementIndex).removeClass(disableClass);
        $('table[name=bf-on-off-table] td:nth-child('+columnIndex+')').removeClass(disableClass);
        $('table[name=bf-on-off-table] td:nth-child('+columnIndex+') textarea, table td:nth-child('+columnIndex+') input[type=radio]').prop('disabled','');
      }else {
        $('table[name=bf-on-off-table] th').eq(elementIndex).addClass(disableClass);
        $('table[name=bf-on-off-table] td:nth-child('+columnIndex+')').addClass(disableClass);
        $('table[name=bf-on-off-table] td:nth-child('+columnIndex+') textarea, table td:nth-child('+columnIndex+') input[type=radio]').prop('disabled','disabled');
      }
      $('table[name=bf-on-off-table] tr:last td').removeClass(disableClass);
      $('table[name=bf-on-off-table] tr:last td').css('background','');
    });

  });

  /* Override Codes */

  function contentWidth() {
    ww = $(window).width();
    $('.bf-content')
    .width(ww-$('.bf-content').css('margin-left').replace('px','')-60);
  }

  function onSuccess(){
    console.log('OK');
  }
  function onFailure(){
    console.log('Error');
  }
    
function submitPopupForm(submitUrl,submitObject){

  $.ajax({
    type: 'POST', 
    url: submitUrl,
    dataType: 'json',
    contentType: 'json',
    headers: submitObject,
    success: function(){
      
    },
    error: onFailure
  });

}

function updateMachineForm(submitUrl,cellObject){

  $.ajax({
    type: 'PUT', 
    url: submitUrl,
    dataType: 'json',
    contentType: 'json',
    headers: cellObject,
    success: onSuccess,
    error: onFailure
  });

}

function addToChangedIDs(elementIndex){
  if (changedColumIds.indexOf(elementIndex) == -1) {
    changedColumIds.push(elementIndex);
  }
  console.log(changedColumIds);
}

function changedObject(idList){
  var allChangedColumns = [];
  var tempCell;
  $.each(idList, function(index,value){
    tempCell = columnValue(value);
    allChangedColumns.push(tempCell);
  });
  return allChangedColumns;
}

function columnValue(cID){
  var cell = {};
  cell.id = $('th').eq(cID).attr('data-id');
  cell.name = $('#col'+cell.id+'_name').text();
  cell.desc =  $('textarea[name="cell'+cell.id+'_desc"]').val();
  cell.column_type = $('#cell'+cell.id+':checkbox:checked').length ? $('input[name="cell'+cell.id+'_column_type"]:checked').attr('data-val') : 'IGN' ;

//  cell.name = 'erdem';
//  cell.column_type =  "OUT";
//  cell.desc= "Description text here";

  return cell;
}

function saveColumn(indexOfColumn) {
  var csrftoken = $("input[name=csrf]").val();
  var cValue = columnValue(indexOfColumn);

  if (cValue.column_type == 'IN'){
    columnType = 'Input';
  }else if(cValue.column_type == 'OUT'){
    columnType = 'Output';
  }else {
    columnType = 'Ignore';
  }

  $('.i-column-type-line').eq(indexOfColumn).html(columnType);

  $.ajax({
    url: '/api/column/'+cValue.id+'/',
    type: 'PUT',
    data: cValue,
    headers: {
      'X-CSRFToken': csrftoken
    },
    success: function(response) {
      console.log(response);
      bottomButton('Next','','green');
      return true;
    },
    error: function(error){
      console.log(error);
      return false;
    }
 });
}
function bottomButton(textValue,addClass,removeClass){
  $('a[name="saveMachine"]')
  .addClass(addClass)
  .removeClass(removeClass)
  .text(textValue);

}

function toDisable(){
  $('.bf-disabled').each(function(){
    $(this)
      .addClass(disableClass)
      .attr('disabled','disabled');
    $(this)
      .find('textarea')
      .attr('disabled','disabled');
    $(this)
      .find('input')
      .attr('disabled','disabled');
    $('.bf-on-off-machine')
      .removeClass(disableClass)
      .removeAttr('disabled');
    
  });
}

function updateBeforeLoading(){
  /*
  $('.updateBeforeLoading').each(function(){
    allTrs = $(this).find('tr').length;
    allTds = $(this).find('td').length;
    allColumns = allTds / (allTrs-1);
    console.log(allColumns);
    for(i=0;i<allColumns;i++){
      saveColumn(i);
    }
  });
  */
}

function loadInlinePages(){
  $('div').each(function(){
    if ($(this).attr('data-inline-modal')){
      inline_url = $(this).attr('data-inline-modal');
      console.log(inline_url);
      $(this).load(inline_url);
    }
  });
}

function openPopup(url){
let params = `scrollbars=no,resizable=no,status=no,location=no,toolbar=no,menubar=no,
width=600,height=300,left=100,top=100`;

open(url, 'test', params);
}

function submitModal(){

  $.ajax({
      url: '/team/add/',
      type: 'post',
      dataType: 'json',
      data: $('#modalSubmit').serialize(),
      success: function(data) {
        console.log('Success : ' + data);
        window.location.href = window.location.href;
      },
      error: function(data) {
        console.log(data);
        window.location.href = window.location.href;
      }

  });

}