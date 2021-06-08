const tabs_data = [
    {
        title: 'TYR',
        video: 'TYR_vid.mp4',
        audio: {
            'END2END': 'TYR_END2END.wav',
            'HBONDS': 'TYR_HBONDS.wav',
            'RGYR': 'TYR_RGYR.wav',
            'STRUCE': 'TYR_STRUCE.wav',
        },
    },
    {
	title: 'TYN',
	video: 'TYN_vid.mp4',
	audio: {
	'END2END': 'TYN_END2END.wav',
	'HBONDS': 'TYN_HBONDS.wav',
	'RGYR': 'TYN_RGYR.wav',
	'STRUCE': 'TYN_STRUCE.wav',
        },
    },
    {
	title: 'TYC',
	video: 'TYC_vid.mp4',
	audio: {
	'END2END': 'TYC_END2END.wav',
	'HBONDS': 'TYC_HBONDS.wav',
	'RGYR': 'TYC_RGYR.wav',
	'STRUCE': 'TYC_STRUCE.wav',
        },
    },


]



function main() {
    tabs_data.forEach(create_tab)
}

function create_tab(tab_data) {
    // create navigation button
    const navigation_button = $('<div class="navigation__button unselectable" />')
    navigation_button.text(tab_data.title)
    navigation_button.on('click', () => open_tab(navigation_button, tab_data.title))
    $('.navigation').append(navigation_button)

    // create tab
    const tab_template = $('#tab--template').html()
    const tab = $(tab_template)
    tab.attr('id', tab_data.title)

    // set video source
    const video = tab.children('.tab__video')
    const source = $('<source />')
    source.attr('src', `media/${tab_data.video}`)
    video.append(source)

    // create audio toggles
    const audio = tab.children('.tab__audio')
    const audio_toggles = []
    Object.entries(tab_data.audio).forEach(([title, file]) => {
        const audio_toggle = $('<div class="tab__audiotoggle unselectable" />')
        audio_toggle.text(title)
        audio_toggle.on('click', () => {
            audio_toggle.toggleClass('tab__audiotoggle--active')
            const active = audio_toggle.hasClass('tab__audiotoggle--active')
            const video_playing = !video[0].paused
            if (video_playing) {
                if (active) {
                    play_audio(audio_toggle, video[0].currentTime)
                } else {
                    pause_audio(audio_toggle)
                }
            }
        })

        const audio_player = $('<audio class="tab__audioplayer" />')
        const source = $('<source />')
        source.attr('src', `media/${file}`)
        audio_player.append(source)
        audio_toggle.append(audio_player)

        audio.append(audio_toggle)
        audio_toggles.push(audio_toggle)
    })

    // setup play/pause events
    video.on('play', () => on_play_video(audio_toggles, video[0].currentTime))
    video.on('pause', () => on_pause_video(audio_toggles))

    // add to page
    const container = $('.container')
    container.append(tab)
    if (container.children().length === 1) {
        open_tab(navigation_button) // if this is the first/only tab, open it by default
    }
}

function open_tab(navigation_button) {
    // hide all tabs
    $('.tab').removeClass('tab--active')

    // deactivate all navigation buttons
    $('.navigation__button').removeClass('navigation__button--active')

    // show current tab, and activate selected navigation button
    $(`#${navigation_button.text()}`).addClass('tab--active')
    navigation_button.addClass('navigation__button--active')
}

function on_play_video(audio_toggles, start_time) {
    audio_toggles.forEach(audio_toggle => play_audio(audio_toggle, start_time))
}

function play_audio(audio_toggle, start_time) {
    if (audio_toggle.hasClass('tab__audiotoggle--active')) {
        const audio_player = audio_toggle.children('.tab__audioplayer')
        audio_player[0].currentTime = start_time
        audio_player[0].play()
    }
}

function on_pause_video(audio_toggles) {
    audio_toggles.forEach(pause_audio)
}

function pause_audio(audio_toggle) {
    const audio_player = audio_toggle.children('.tab__audioplayer')
    audio_player[0].pause()
}

$(main)