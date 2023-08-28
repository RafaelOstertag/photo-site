jQuery("#lightgallery")
    .justifiedGallery({
        captions: false,
        lastRow: "center",
        rowHeight: 180,
        margins: 5
    })
    .on("jg.complete", function () {
        window.lightGallery(
            document.getElementById("lightgallery"),
            {
                autoplayFirstVideo: false,
                pager: false,
                galleryId: "nature",
                plugins: [lgThumbnail,lgFullscreen,lgZoom],
                mobileSettings: {
                    controls: false,
                    showCloseIcon: false,
                    download: true,
                    rotate: true
                }
            }
        );
    });