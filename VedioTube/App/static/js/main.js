$(document).ready(function(){
	$(".videoPlayer").toArray().forEach(function(videoPlayer){
		var video = $(videoPlayer).find("video")[0];
		var playPauseBtn = $(videoPlayer).find(".playPauseBtn");
		var fullscreen = $(videoPlayer).find(".fullscreen");
		var startTime = $(videoPlayer).find(".startTime");
		var endTime = $(videoPlayer).find(".endTime");
		var playerSeekBar = $(videoPlayer).find(".topControls .seekbar");
		var playerProgressBar = $(videoPlayer).find(".topControls .seekbar .progressBar");
		var volumeSeekBar = $(videoPlayer).find(".volumeCtrl .seekbar");
		var volumeProgressBar = $(videoPlayer).find(".volumeCtrl .seekbar .progressBar");
		var volumePercentage = $(videoPlayer).find(".volumeCtrl .percentage");
		var fastForward = $(videoPlayer).find(".forward");
		var fastBackward= $(videoPlayer).find(".backward");

		var currentDuration,endDuration,seekBarPercentage,interval,completeDuration;

		/* Onclick function  */
		$(playPauseBtn).on("click",function(){
			completeDuration = video.duration;
			endDuration = calculateDuration(completeDuration);
			endTime.text(
				`${endDuration.hours}:${endDuration.minutes}:${endDuration.seconds}`
				);
			console.log(endDuration.minutes);

	if(playPauseBtn.hasClass("play")){
		video.play();
		playPauseBtn.addClass("pause").removeClass("play");
		$(videoPlayer).addClass("isPlaying");
	}
	else if(playPauseBtn.hasClass("pause")){
		video.pause();
		playPauseBtn.addClass("play").removeClass("pause");
		$(videoPlayer).removeClass("isPlaying");
	}
	interval = setInterval(function(){
		if(!video.paused){
			updateSeekBar();
		}
		if(video.paused){
			clearInterval(interval);
		}
		if(video.ended){
			clearInterval(interval);
			$(playerProgressBar).css("width","100%");
			playPauseBtn.removeClass("pause").addClass("play");
			$(videoPlayer).removeClass("isPlaying").addClass("showControls");
		}
	},500);
	
		});

		/* fast backward*/
		fastBackward.on("click",function(){
			if(!video.ended && completeDuration != undefined){
				video.currentTime>0 && video.currentTime<video.duration?(video.currentTime-=10):0;
			}
		});

		/* fast forward */
		fastForward.on("click",function(){
			if(!video.ended && completeDuration != undefined){
				video.currentTime>0 && video.currentTime<video.duration?(video.currentTime+=10):0;
			}
		});	

		/* seekbar */
		playerSeekBar.on("click",function(e){
			if(!video.ended && completeDuration != undefined){
				var seekPosition = e.pageX - $(playerSeekBar).offset().left;
				if(seekPosition>=0 && seekPosition<$(playerSeekBar).outerWidth()){
					video.currentTime = (seekPosition*completeDuration)/$(playerSeekBar).outerWidth();
					updateSeekBar();
				}
			}
		});

		/* volume percentage*/
		volumeSeekBar.on("click",function(e){
			var volumePosition = e.pageX - $(volumeSeekBar).offset().left;
			var videoVolume = volumePosition / $(volumeSeekBar).outerWidth();
			if(videoVolume>=0 && videoVolume<=1){
				video.volume = videoVolume;
				volumeProgressBar.css("width",videoVolume*100+"%");
				volumePercentage.text(Math.floor(videoVolume*100)+"%");
			}
		});

		/* full screen */
		fullscreen.on("click",function(e){
			if(video.requestFullscreen){
				video.requestFullscreen();
			}
			else if(video.webkitRequestFullscreen){
				video.webkitRequestFullscreen();
			}
		});
		
		/* toggle controls */
		$(videoPlayer).hover(function(){
			if($(videoPlayer).hasClass("isPlaying")){
				$(videoPlayer).addClass("showControls");
			}
		},function(){
			setTimeout(function(){
				if($(videoPlayer).hasClass("isPlaying")){
					$(videoPlayer).removeClass("showControls");
			}
		},2000);
		}
	);

		var updateSeekBar = function(){
			seekBarPercentage = getPercentage(video.currentTime,video.duration);
			currentDuration = calculateDuration(video.currentTime);
			startTime.text(`${currentDuration.hours}:${currentDuration.minutes}:${currentDuration.seconds}`);
			$(playerProgressBar).css("width",seekBarPercentage+"%");
		};
	
	});
	var getPercentage = function(presentTime,totallength){
		var calcPercentage = (presentTime/totallength)*100;
		console.log(calcPercentage);
		return parseFloat(calcPercentage.toString());
	};
	var calculateDuration = function(duration){
		var seconds = parseInt(duration%60);
		var minutes = parseInt((duration%3600)/60);
		var hours = parseInt(duration/3600);
		return{
			hours:pad(hours),
			minutes:pad(minutes.toFixed()),
			seconds:pad(seconds.toFixed())
		};
	};
	var pad = function(number){
		if(number > -10 && number < 10){
			return "0"+number;
		}
		else{
			return number;
		}
	}
});

function myFunction(x) {
  x.classList.toggle("fa-thumbs-down");
}

$('.likebutton').click(function(){ 
	var id; 
	id = $(this).attr("data-catid"); 
	$.ajax( 
	{ 
		type:"GET", 
		url: "like", 
		data:{ 
				 post_id: id 
	}, 
	success: function( data ) 
	{ 
		$( '#like'+ id ).removeClass('btn btn-primary btn-lg'); 
		$( '#like'+ id ).addClass('btn btn-success btn-lg'); } }) 
	});