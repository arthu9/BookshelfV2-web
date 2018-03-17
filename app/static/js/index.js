/* Simple Tabs by Example
 * @author Chatman Richmond Jr.
 * Details: Exactly what it says on the tin. A simple, but not bulletproof, method for tabbed content.
 * The code is written to make adding new tabs a breeze. It was a fun experiment, anyway.
 * I'm loving Codepen, so expect more soon.
 */


var CHATRJR = {
  // Engage tabs!
  tabTrigger: function () {
    /* Helper Variables
     * @tabs: grabs the tab links
     * @tabsLength: cached length of tabs
     * @content: content to be toggled
     */
    var linkCount,
        tabs = $('.tab a'),
        tabsLength = tabs.length,
        content = $('.tab-content-wrap'),
        // @clickIterator: responsible for sorting the click events for individual tabs
        // I'm aware I could have used the each() method.
        clickIterator = function (item) {
          // click event to fire the tab toggle
          tabs.eq(item).on('click', function(e) {
            e.preventDefault();
            // active tab has its class removed and visible content is hidden
            if (tabs.hasClass('active-tab')) {
              tabs.removeClass('active-tab');
            }
            // new active tab is triggered and content slides into place
            tabs.eq(item).addClass('active-tab');
            content.removeClass('active-tab').slideUp(500);
            content.eq(item).addClass('active-tab').slideDown(500);
          });
        };
    // special loop that iterates over the tab links and content
    // without exceeding the total tabs
    for(linkCount = 0; linkCount < tabsLength; linkCount += 1) {
      clickIterator(linkCount);
    }
  }
};

CHATRJR.tabTrigger();














$(document).ready(function(){


	//----------Select the first tab and div by default

	$('#vertical_tab_nav > ul > li > a').eq(0).addClass( "selected" );
	$('#vertical_tab_nav > div > article').eq(0).css('display','block');


	//---------- This assigns an onclick event to each tab link("a" tag) and passes a parameter to the showHideTab() function

		$('#vertical_tab_nav > ul').click(function(e){

      if($(e.target).is("a")){

        /*Handle Tab Nav*/
        $('#vertical_tab_nav > ul > li > a').removeClass( "selected");
        $(e.target).addClass( "selected");

        /*Handles Tab Content*/
        var clicked_index = $("a",this).index(e.target);
        $('#vertical_tab_nav > div > article').css('display','none');
        $('#vertical_tab_nav > div > article').eq(clicked_index).fadeIn();

      }

        $(this).blur();
        return false;

		});


});//end ready


//-----------------NOTIFICATION BUTTON--------------------------

			$(document).ready(function()
			{
			$("#notificationLink").click(function()
			{
			$("#notificationContainer").fadeToggle(800);
			$("#notification_count").fadeOut("slow");
			return false;
			});

			//Document Click hiding the popup
			$(document).click(function()
			{
			$("#notificationContainer").hide();
			});

			//Popup on click
			$("#notificationContainer").click(function()
			{
			return false;
			});

			});



