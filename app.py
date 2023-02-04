from youtube_transcript_api import YouTubeTranscriptApi
from flask import Flask, render_template
from flask import render_template, request, redirect, url_for, flash, send_file, session, copy_current_request_context
from pytube import YouTube
from io import BytesIO
import os, os.path
import logging
import threading


app = Flask(__name__)

#Setting the secret key. It is used to encrypt cookies and save send them to the browser
app.config['SECRET_KEY'] = 'helloworld'

#App Routing mapping the URLs to a specific function.
@app.route('/')
def main():
    """Main function is rendering index.html (home page) of my web application MA Online Video Downloader."""
    return render_template('index.html')
   
@app.route('/bulkdownload')
def bulkdownload():
    """Bulk Download function is rendering bulkdownload.html page of my web application MA Online Video Downloader."""
    return render_template('bulkdownload.html')
    
@app.route('/audiodownload')
def audiodownload():
    """Audio Download function is rendering audiodownload.html page of my web application MA Online Video Downloader."""
    return render_template('audiodownload.html')

@app.route('/transcript')
def transcript():
    """Transcript Download function is rendering transcript.html page of my web application MA Online Video Downloader."""
    return render_template('transcript.html')


@app.route("/", methods = ["GET", "POST"])
@app.route("/index", methods = ["GET", "POST"])
def index():
    """When the form is submitted, the video link is
    parsed and made ready for download."""
    if request.method == "POST":

        #Getting the URL of a YouTube video from user submitted form.
        session['link'] = request.form.get('url')

        try:
            #Creating a session with YouTube with Link provided by User.
            url = YouTube(session['link'])

            #Checking the validity/availability of YouTube URL.
            url.check_availability()

            # The purpose of this function is to find the length of the video in hours, minutes, seconds
            def find_video_length():

                # Getting the total length of video in seconds
                duration = url.length
                
                # Hours are calculated by dividing the total seconds with 3600.
                # 1 hour = 60 mins
                # 1 min = 60 seconds
                # 1 hour = 60 * 60 = 3600 seconds
                hours = duration // 3600
                hours = int(hours)
                
                # Minutes are calculated by subtracting the hours from total duration and dividing it with 60.
                minutes = (duration - hours * 3600) // 60
                minutes = int(minutes)

                # Seconds are calculated by dividing the total seconds with 60 and storing the remainder.
                seconds = duration % 60
                seconds = int(seconds)

                #If hours are less than 10 add extra 0 on left side like 01, 02 upto 09
                if hours<10:
                    hours = str(0) + str(hours)
                
                #If minutes are less than 10 add extra 0 on left side like 01, 02 upto 09
                if minutes<10:
                    minutes = str(0) + str(minutes)

                #If seconds are less than 10 add extra 0 on left side like 01, 02 upto 09
                if seconds<10:
                    seconds = str(0) + str(seconds)

                # Concatenating the hours : minutes : seconds format (String)
                video_length = str(hours) + ":" + str(minutes) + ":" + str(seconds)
                return video_length

            # The purpose of this function is to calculate the size of the video in GBs or MBs.
            def get_video_file_size():
                
                # Get the video file size
                file_size = url.streams.get_highest_resolution().filesize

                # Converting the file size into GBs
                video_file_size_GB = round(file_size / (1024 * 1024 * 1024), 2)
                
                # Converting the file size into MBs
                video_file_size_MB = round(file_size / (1024 * 1024), 2)

                # Convert video file size into GB string if  video_file_size_GB is greater than 1 less convert video file size into MBs String
                best_video_file_size = str(video_file_size_GB) + ' GB' if video_file_size_GB > 1 else str(video_file_size_MB) + ' MB'
                return best_video_file_size
            
            # Call find_video_length function to calculate the duration of the video
            video_duration = find_video_length()

            # Call get_video_file_size function to calculate the size of the video
            video_file_size = get_video_file_size()

            # Streaming all the mp4 videos of Progressive stream. The highest resolution in this stream is 720p.
            resolution = url.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
            
        except:
            # If there an any issue with URL a flash message will be pop up with message 'Error: Invalid link or no link provided'
            flash('Error: Invalid link or no link provided')

            return redirect(url_for('index'))

        # If URL is valid and available and video size and duration is calculated than render_template function will render videodownload.html and display all the information related to video to the user.
        return render_template(
            "videodownload.html",
            url=url,
            video_duration=video_duration,
            hightest_resolution=resolution.resolution,
            best_video_file_size=video_file_size)
    return render_template("index.html", title="Home")


@app.route("/audiodownload", methods = ["GET", "POST"])
def mp3download():
    """When the form is submitted, the video link is
    parsed and made ready for download."""

    if request.method == "POST":
        
        #Getting the URL of a YouTube video from user submitted form.
        session['link'] = request.form.get('url')
        
        try:
            #Creating a session with YouTube with Link provided by User.
            url = YouTube(session['link'])

            #Checking the validity/availability of YouTube URL.
            url.check_availability()

            # The purpose of this function is to find the length of the video in hours, minutes, seconds
            def find_audio_length():
                
                # Getting the total length of video in seconds
                duration = url.length
                
                # Hours are calculated by dividing the total seconds with 3600.
                # 1 hour = 60 mins
                # 1 min = 60 seconds
                # 1 hour = 60 * 60 = 3600 seconds
                hours = duration // 3600
                hours = int(hours)
                
                # Minutes are calculated by subtracting the hours from total duration and dividing it with 60.
                minutes = (duration - hours * 3600) // 60
                minutes = int(minutes)

                # Seconds are calculated by dividing the total seconds with 60 and storing the remainder.
                seconds = duration % 60
                seconds = int(seconds)

                #If hours are less than 10 add extra 0 on left side like 01, 02 upto 09
                if hours<10:
                    hours = str(0) + str(hours)
                
                #If minutes are less than 10 add extra 0 on left side like 01, 02 upto 09
                if minutes<10:
                    minutes = str(0) + str(minutes)

                #If seconds are less than 10 add extra 0 on left side like 01, 02 upto 09
                if seconds<10:
                    seconds = str(0) + str(seconds)

                # Concatenating the hours : minutes : seconds format (String)
                audio_length = str(hours) + ":" + str(minutes) + ":" + str(seconds)
                return audio_length

            # The purpose of this function is to calculate the size of the audio in GBs or MBs.
            def get_audio_file_size():

                # Get the audio file size
                file_size = url.streams.get_audio_only().filesize#filter(only_audio=True)
                
                # Converting the file size into GBs
                audio_file_size_GB = round(file_size / (1024 * 1024 * 1024), 2)
                
                # Converting the file size into MBs
                audio_file_size_MB = round(file_size / (1024 * 1024), 2)
                
                # Convert audio file size into GB string if  audio_file_size_GB is greater than 1 less convert audio file size into MBs String
                best_audio_file_size = str(audio_file_size_GB) + ' GB' if audio_file_size_GB > 1 else str(audio_file_size_MB) + ' MB'
                return best_audio_file_size
            
            # Call find_audio_length function to calculate the duration of the audio
            audio_duration = find_audio_length()

            # Call get_audio_file_size function to calculate the size of the audio file
            audio_file_size = get_audio_file_size()
            
        except:
            # If there an any issue with URL a flash message will be pop up with message 'Error: Invalid link or no link provided'
            flash('Error: Invalid link or no link provided')

            return redirect(url_for('index'))

        # If URL is valid and available and audio size and duration is calculated than render_template function will render mp3download.html and display all the information related to audio to the user.
        return render_template(
            "mp3download.html",
            url=url,
            audio_duration=audio_duration,
            best_audio_file_size=audio_file_size)
    return render_template("index.html", title="Home")


@app.route("/transcript", methods = ["GET", "POST"])
def downloadtrans():
    """When the form is submitted, the video link is
    parsed and made ready for download."""

    if request.method == "POST":

        #Getting the URL of a YouTube video from user submitted form.
        session['link'] = request.form.get('url')

        try:
            #Creating a session with YouTube with Link provided by User.
            url = YouTube(session['link'])
            
            #Checking the validity/availability of YouTube URL.
            url.check_availability()

            # The purpose of this function is to find the length of the video in hours, minutes, seconds
            def find_audio_length():
            
                # Getting the total length of video in seconds
                duration = url.length
                
                # Hours are calculated by dividing the total seconds with 3600.
                # 1 hour = 60 mins
                # 1 min = 60 seconds
                # 1 hour = 60 * 60 = 3600 seconds
                hours = duration // 3600
                hours = int(hours)
                
                # Minutes are calculated by subtracting the hours from total duration and dividing it with 60.
                minutes = (duration - hours * 3600) // 60
                minutes = int(minutes)

                # Seconds are calculated by dividing the total seconds with 60 and storing the remainder.
                seconds = duration % 60
                seconds = int(seconds)

                #If hours are less than 10 add extra 0 on left side like 01, 02 upto 09
                if hours<10:
                    hours = str(0) + str(hours)
                
                #If minutes are less than 10 add extra 0 on left side like 01, 02 upto 09
                if minutes<10:
                    minutes = str(0) + str(minutes)

                #If seconds are less than 10 add extra 0 on left side like 01, 02 upto 09
                if seconds<10:
                    seconds = str(0) + str(seconds)

                # Concatenating the hours : minutes : seconds format (String)
                audio_length = str(hours) + ":" + str(minutes) + ":" + str(seconds)
                return audio_length

            
            # Call find_audio_length function to calculate the duration of the audio
            audio_duration = find_audio_length()
            
        except:
            # If there an any issue with URL a flash message will be pop up with message 'Error: Invalid link or no link provided'
            flash('Error: Invalid link or no link provided')

            return redirect(url_for('index'))

        # If URL is valid and available and audio duration is calculated than render_template function will render transcriptdownload.html and display all the information related to video to the user.
        return render_template(
            "transcriptdownload.html",
            url=url,
            audio_duration=audio_duration
            #best_audio_file_size=audio_file_size
            )
    return render_template("index.html", title="Home")



@app.route("/videodownload", methods = ["GET", "POST"])
def downloadvideo():
    """When user clicks on Download Video button, Video will be Downloaded and saved to the user's computer"""
    
    if request.method == "POST":

        # Creare a buffer of type ByteIO for storing video streaming
        buffer = BytesIO()

        # Creating a session with YouTube with Link provided by User.
        url = YouTube(session['link'])
        
        # Get the video title from URL
        file_name = url.title + ".mp4"
        
        # Stream video of highest available resolution 
        myvideo = url.streams.get_highest_resolution()
        
        # Saving streamed video into buffer
        myvideo.stream_to_buffer(buffer)

        # Change the position of the File Handle to a given specific position.
        # File handle is like a cursor, which defines from where the data has to be read or written in the file. 
        # In this case start of the file
        buffer.seek(0)

        # Transfers the contents of a file to the client 
        return send_file(
            buffer,
            download_name=file_name,
            as_attachment=True, 
            mimetype='video/mp4'
        )
    return redirect(url_for("videodownload"))

@app.route("/index", methods = ["GET", "POST"])
def gobackhome():
    if request.method == "POST":
        return render_template("index.html")




@app.route("/mp3download", methods = ["GET", "POST"])
def downloadmp3():
    """When user clicks on Download Audio button, Audio will be Downloaded and saved to the user's computer"""
    
    try:

        if request.method == "POST":

            # Creare a buffer of type ByteIO for storing audio streaming
            buffer = BytesIO()
            
            # Creating a session with YouTube with Link provided by User.
            url = YouTube(session['link'])

            # Get the video title from URL
            file_name = url.title + ".mp3"
        
            #itag = request.form.get("itag")
            # Stream audio from the video URL 
            myaudio = url.streams.get_audio_only()#get_highest_resolution()#.get_by_itag(itag)
            #myvideo.download()

            # Saving streamed audio into buffer
            myaudio.stream_to_buffer(buffer)

            # Change the position of the File Handle to a given specific position.
            # File handle is like a cursor, which defines from where the data has to be read or written in the file. 
            # In this case start of the file
            buffer.seek(0)
            
            # Transfers the contents of a file to the client 
            return send_file(
                buffer,
                download_name=file_name,
                as_attachment=True, 
                mimetype='audio/mp3'
            )
        return render_template('mp3download')
        

    except Exception as ex:
        logging.warning("Exception: " + ex)


@app.route("/transcriptdownload", methods = ["GET", "POST"])
def downloadtranscript():
    """Downloads the transcript and saves it to the user's computer"""
    try:

        if request.method == "POST":
            buffer = BytesIO()
            url = YouTube(session['link'])
            file_name = url.title + "_Transcript.txt"
            #itag = request.form.get("itag")

            # The purpose of this function is to find the length of the video in hours, minutes, seconds
            def find_audio_length():
                
                # Getting the total length of video in seconds
                duration = url.length
                
                # Hours are calculated by dividing the total seconds with 3600.
                # 1 hour = 60 mins
                # 1 min = 60 seconds
                # 1 hour = 60 * 60 = 3600 seconds
                hours = duration // 3600
                hours = int(hours)
                
                # Minutes are calculated by subtracting the hours from total duration and dividing it with 60.
                minutes = (duration - hours * 3600) // 60
                minutes = int(minutes)

                # Seconds are calculated by dividing the total seconds with 60 and storing the remainder.
                seconds = duration % 60
                seconds = int(seconds)

                #If hours are less than 10 add extra 0 on left side like 01, 02 upto 09
                if hours<10:
                    hours = str(0) + str(hours)
                
                #If minutes are less than 10 add extra 0 on left side like 01, 02 upto 09
                if minutes<10:
                    minutes = str(0) + str(minutes)

                #If seconds are less than 10 add extra 0 on left side like 01, 02 upto 09
                if seconds<10:
                    seconds = str(0) + str(seconds)

                # Concatenating the hours : minutes : seconds format (String)
                audio_length = str(hours) + ":" + str(minutes) + ":" + str(seconds)
                return audio_length

            # Call find_audio_length function to calculate the duration of the audio
            audio_duration = find_audio_length()
    
        
            # For Testing Purpose
            # Video Id: SW14tOda_kI
            # srt = YouTubeTranscriptApi.get_transcript("SW14tOda_kI",languages=['en'])

            # For Testing Purpose
            # https://youtu.be/Nn_iCKa7neM
            srt = YouTubeTranscriptApi.get_transcript(url.video_id)#,languages=['en'])

            # Get the username of the user who is currently logged in
            username = os.getlogin()
            
            # Creating or overwriting a file "Video_Title + - Transcript.txt" with
            # the info inside the context manager
            with open(f'C:/Users/{username}/Downloads/'+ url.title +" - Transcript.txt", "w") as f:
   
            # Iterating through each element of list srt
                for i in srt:
                    # writing each element of srt on a new line
                    f.write("{}\n".format(i))

            # If Trascript of a video is downloaded successfully a flash message will be pop up with message 'Transcript downloaded successfully. Please check your Downloads Folder.'
            flash("Transcript downloaded successfully. Please check your Downloads Folder")
            
    except Exception as ex:

        # If Trascript of a video is not available a flash message will be pop up with message 'Trascript Not Found for this video.'
        flash("Trascript Not Found for this video.")
        logging.exception(ex)
    
    finally:

        # If URL is valid and available and audio duration is calculated than render_template function will render transcriptdownload.html and display all the information related to video to the user.
        return render_template(
            "transcriptdownload.html",
            url=url,
            audio_duration=audio_duration,
            #best_audio_file_size=0
            )


@app.route('/bulkdownload', methods = ["GET", 'POST'])  
def bulkdownloadvideo():  
    """Downloads the videos in bulk and saved it to the user's computer"""
    
    if request.method == 'POST':
        
        #Getting the file uploaded by user.
        f = request.files['file']
        
        # Getting the file name of the file uploaded by user.
        filename = f.filename

        # Saving the file uploaded by user on current working directory where application is running.
        f.save(f.filename) 

        @copy_current_request_context
        def background_task(link):
            """The purpose of Background Task function is to download video in bulk video downloading functionality.
            Start separate thread to download video against YouTube URL provided in the file.
            """
    
            try:
                
                #Creating a session with YouTube with Link read from file.
                url = YouTube(link)
                
                # Stream video of highest available resolution 
                myvideo = url.streams.get_highest_resolution()
                
                # Get the username of the user who is currently logged in
                username = os.getlogin()

                # Downloading the video to user's download folder.
                myvideo.download(f'C:/Users/{username}/Downloads')

                # Once video is downloaded a pop message will appear video is downloaded. Please check your Downloads folder.
                flash(url.title + " is downloaded. Please check your Downloads folder")
                
            except Exception as ex:
                logging.warning("Exception: "+ str(ex))

        # Setting download_flag to True to run the while loop till the last URL in the file. 
        download_flag = True

        while download_flag:
            try:

                # Opening file uploaded by user
                with open(filename) as file:

                    # Read line by line from file and loop through till last URL.
                    for line in file:

                        # Removing extra spaces (leading & trailing) from line and convert into String
                        link = str(line).strip()

                        # Start separate thread for downloading each video. 
                        th = threading.Thread(target=background_task, args=(link,))
                        th.daemon = True
                        th.start()
                        th.join() # Blocking the current thread (main thread) until the target thread that has been joined has terminated.

                # Set download_flag to False when all the URL are accessed/read from the file (means end of the file).  
                download_flag = False

            except Exception as ex:
                logging.warning("Exception: "+ str(ex))

            finally:
                download_flag = False

        return render_template("bulkdownload.html", name = f.filename)

if __name__=="__main__":
    app.run(debug=True)