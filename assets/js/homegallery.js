jQuery(".homeGallery")
    .justifiedGallery({
        captions: true,
        //maxRowHeight: 200,
        lastRow: "center",
        rowHeight: 150,
        margins: 5
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