jQuery("#lightgallery")
    .justifiedGallery({
        captions: false,
        lastRow: "hide",
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
                plugins: [lgThumbnail],
                mobileSettings: {
                    controls: false,
                    showCloseIcon: false,
                    download: false,
                    rotate: false
                }
            }
        );
    });