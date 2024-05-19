console.log('hello')
/* Set the width of the side navigation to 300px */
function openNav() {
    document.getElementById("mySidenav").style.width = "300px";
  }
  
  /* Set the width of the side navigation to 0 */
  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
  }

  // to show password at login from
  function myFunction() {
    var show_passsword = document.getElementById("showinput");
    if (show_passsword.type === "password") {
      show_passsword.type = "text";
    } else {
      show_passsword.type = "password";
    }
  }

  function myFunctionshowmanufacturerpasswordinput() {
    var show_passsword = document.getElementById("showmanufacturerpasswordinput");
    if (show_passsword.type === "password") {
      show_passsword.type = "text";
    } else {
      show_passsword.type = "password";
    }
  }

  function myFunctionshowvendorpasswordinput() {
    var show_passsword = document.getElementById("showvendorpasswordinput");
    if (show_passsword.type === "password") {
      show_passsword.type = "text";
    } else {
      show_passsword.type = "password";
    }
  }
  
  //code to enter only text in text feild restrict number
  $('.mytext').on('input', function() {
    var input = $(this).val();
    var letters = input.replace(/[^a-zA-Z]/g, '');
    $(this).val(letters);
  });


  function dateFunction(){
    const today = new Date()
    // console.log(today)
    const date = today.getDate();
    const month = today.getMonth() + 1;
    const year = today.getFullYear();
    document.getElementById("saleOrderDate").value = `${year}/${month}/${date}`;


  }


  function myDateFunction() {
    let saleOrderDate = document.getElementById("saleOrderDate").value;
    let expectedShipmentDate = document.getElementById("expectedShipmentDate").value;
    console.log(saleOrderDate)
    console.log(expectedShipmentDate)

    if(saleOrderDate > expectedShipmentDate){
      console.log('Given date is greater than the current date.');
    }else{
      alert('Given date is not greater than the current date.');
    }
  }



// for dropdown in manufacturer dashboard
  var dropdown = document.getElementsByClassName("dropdown-btn");
  var i;

for (i = 0; i < dropdown.length; i++) {
  dropdown[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var dropdownContent = this.nextElementSibling;
    if (dropdownContent.style.display === "block") {
      dropdownContent.style.display = "none";
    } else {
      dropdownContent.style.display = "block";
    }
  });
}

function add_single_item_click(){
  $('#item_name_dropdown').hide();
  $('#item_name').hide();
  $('#item_name_div').hide();
  $('#stock').hide();
  $('#stock_dropdown').hide();
  $('#stock_div').hide();
  $('#gst_div').hide();
  $('#gst_dropdown').hide();
  $('#gst').hide();
  $('#price').hide();
  $('#price_div').hide();
  $('#price_dropdown').hide();

}

$(window).on('load', function() {
  add_single_item_click();
});

//  adding new rows for product detail page
let auth_token;
$(document).ready(function() {

  $.ajax({
    type: 'get',
    url: 'https://www.universal-tutorial.com/api/getaccesstoken',
    success: function(data) {
      auth_token = data.auth_token
      getCountry(data.auth_token);
    },
    error: function(error) {
    console.log(error);
    },
    headers: {
    "Accept": "application/json",
    "api-token":
    "pOJ5QrTk2Qs3dzb2g8S9zRJthVVjCkE0TiDNHmjhhWgfGYFGDHqTZmB_lnoVtQ2oUCA",
    "user-email": "juzerkathiyawadi53@gmail.com"
    }
    })

    $('.country').change (function () {
      console.log("first")
      getState();
      })

    $('.state').change (function () {
        getCity();
      })
    


    function getCountry (auth_token) {
      $.ajax({
      type: 'get',
      url: 'https://www.universal-tutorial.com/api/countries/',
      success: function(data) {
        console.log(data)
        getState (auth_token)  
        $('.country').append('<option value="'+'India'+'"> '+'India'+ '</option>');
        // data.forEach(element => {
        //   $('.country').append('<option value="'+element.country_name+'"> '+element.country_name+ '</option>');
        //   });
      },
      error: function(error) {
      console.log(error);
      },
      headers: {
      "Authorization": "Bearer "+ auth_token,
      "Accept": "application/json"
      }
      })
      }

      function getState() {
        let country_name = $('.country').val();
        $.ajax({
        type: 'get',
        url: 'https://www.universal-tutorial.com/api/states/'+country_name,
        success: function(data) {
          console.log(data)
        // getCity (auth_token);
        $('.state').empty();
        data.forEach(element => {
          $('.state').append('<option value="'+element.state_name+'"> '+element.state_name+ '</option>');
          });
        },
        error: function(error) {
        console.log(error);
        },
        headers: {
        "Authorization": "Bearer "+ auth_token,
        "Accept": "application/json"
        }
        })
        }

        
        function getCity() {
          let state_name = $('.state').val();
          $.ajax({
          type: 'get',
          url: 'https://www.universal-tutorial.com/api/cities/'+state_name,
          success: function(data) {
          $('.region').empty();
          data.forEach(element => {
          $('.region').append('<option value="'+element.city_name+'">'+element.city_name+ '</option>' );
          });
          },
          error: function(error) {
          console.log(error);
          },
          headers: {
          "Authorization": "Bearer "+ auth_token,
          "Accept": "application/json"
          }
          })
        }

   

  $(".manufacturerUnitName").change(function(){
    console.log('hello')

    var url = $("#salesOrderForm").attr("product-data-url");
    var mf_unit = $(this).val();

    $.ajax({
      url : url,
      data:{
        'manufacturer_unit_name' : mf_unit
      },
      success: function(data){
         $(".product").html(data);
         proddata = data
      }
    });
  }) 

  $(".unitType").change(function(){
    console.log('hello')

    var url = $("#salesOrderForm").attr("load-manufacturer-distributor-url");
    var mf_unit = $(this).val();

    $.ajax({
      url : url,
      data:{
        'distributor' : mf_unit
      },
      success: function(data){
         $(".distManuName").html(data);
      }
    });
  }) 

  $(".unitTypePurchaseOrder").change(function(){
    console.log('hello')

    var url = $("#purchaseOrderForm").attr("load-manufacturer-distributor-url");
    var mf_unit = $(this).val();

    $.ajax({
      url : url,
      data:{
        'distributor' : mf_unit
      },
      success: function(data){
         $(".distManuName").html(data);
      }
    });
  }) 

  // $(".productName").on('change',function(){

  //   var url = $("#salesOrderForm").attr("product-data-length-url");
  //   var product_name = $(this).val();

  //   $.ajax({
  //     url : url,
  //     data:{
  //       'product_name' : product_name
  //     },
  //     success: function(data){
  //       $(".productLength").html(data);
  //       prodlen = data
  //       // $("#productLength"+count).html(data);
  //     }
  //   });
  // })



//  total amount calculation
  $('table tbody').on('change', '.amount', function(){
     console.log("hello world")
    var sum=0;

    $('.amount').each(function(){
      console.log("amount")
    sum+=Number($(this).val()).toFixed(2);
    });

    $('#total').val(sum);

    })

    $(".vendorUnitName").change(function(){
      console.log('hello')
  
      var url = $("#purchaseOrderForm").attr("product-data-url");
      var vendor_unit = $(this).val();
  
      $.ajax({
        url : url,
        data:{
          'vendor_unit_name' : vendor_unit
        },
        success: function(data){
           $(".product").html(data);
           proddata = data
        }
      });
    }) 



    // $('#clickButton').click('',function(){
    //   const today = new Date();
    //   // document.getElementById("saleOrderDate").innerHTML = today;
    //   $("#saleOrderDate").html(today);
  
    //   console.log(today)
    // })

  // Inventory java script

    $(".selectCategoryName").change(function(){
      console.log('hello')
  
      var url = $("#Form").attr("category-data-url");
      var mf_unit = $(this).val();
  
      $.ajax({
        url : url,
        data:{
          'category_load' : mf_unit
        },
        success: function(data){
           $(".category").html(data);
           proddata = data
        }
      });
    }) 


    $(".selectCategoryName").change(function(){
      console.log('hello')
  
      var url = $("#Form").attr("rack-data-url");
      var mf_unit = $(this).val();
  
      $.ajax({
        url : url,
        data:{
          'category_load' : mf_unit
        },
        success: function(data){
           $(".rack").html(data);
           proddata = data
        }
      });
    }) 


    $(".selectpurchaseorder").change(function(){
      console.log('hello')
      
      var url = $("#Form").attr("product-data-url");
      var mf_unit = $(this).val();  
      if(mf_unit != null){
      $('#item_name_div').show();

        $.ajax({
          url : url,
          data:{
            'purchase_order' : mf_unit
          },
          success: function(data){
             $(".product").html(data);
            //  proddata = data
          }
        });

        if(mf_unit != 'others'){
          $('#item_name_dropdown').show()
          $('#item_name').hide()
          $('#stock').hide()
          $('#stock_div').hide();
          $('#gst_div').hide();
          $('#gst').hide();
          $('#price_div').hide();
          $('#price').hide();
          

        }
        else{
          $('#item_name').show()
          $('#item_name_dropdown').hide()
          $('#stock').show()
          $('#stock_dropdown').hide()
          $('#stock_div').show();
          $('#gst').show();
          $('#gst_div').show();
          $('#gst_dropdown').hide();
          $('#price').show();
          $('#price_div').show();
          $('#price_dropdown').hide();


        }
      }
     
      
  
     
    }) 

    $(".itemName").change(function(){
      console.log('hello')
      var url = $("#Form").attr("product-stock-url");
      var mf_unit = $(this).val();
      if(mf_unit != null){
      $.ajax({
        url : url,
        data:{
          'item_name' : mf_unit
        },
        success: function(data){
           $(".productQty").html(data);
          //  document.getElementById("productQty").innerText = data;
          //  proddata = data
        }
      });
    }
    }) 

    $(".itemName").change(function(){
      console.log('hello')
      var url = $("#Form").attr("product-gst-url");
      var mf_unit = $(this).val();
      if(mf_unit != null){
      $.ajax({
        url : url,
        data:{
          'item_name' : mf_unit
        },
        success: function(data){
           $(".productgst").html(data);
          //  document.getElementById("productQty").innerText = data;
          //  proddata = data
        }
      });      
    }
   
    }) 

    $(".itemName").change(function(){
      console.log('hello')
      var url = $("#Form").attr("product-price-url");
      var mf_unit = $(this).val();
      if(mf_unit != null){
      $.ajax({
        url : url,
        data:{
          'item_name' : mf_unit
        },
        success: function(data){
           $(".productprice").html(data);
          //  document.getElementById("productQty").innerText = data;
          //  proddata = data
        }
      });      
    }
   
    }) 
    


  


    

  });
