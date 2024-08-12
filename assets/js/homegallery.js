jQuery(".homeGallery")
    .justifiedGallery({
        captions: true,
        //maxRowHeight: 200,
        lastRow: "center",
        rowHeight: 250,
        margins: 40
    })
    .on("jg.complete", function (evt) {
        window.lightGallery(
            evt.target,
            {
                autoplayFirstVideo: false,
                pager: false,
                galleryId: "light-gallery-" + (Math.floor(Math.random() * 100)),
                plugins: [lgThumbnail, lgFullscreen, lgZoom],
                mobileSettings: {
                    controls: false,
                    showCloseIcon: false,
                    download: true,
                    rotate: true
                }
            }
        );
    });