from skimage import data
from skimage import transform
from skimage.color import rgb2gray
from skimage.feature import match_descriptors, plot_matches, SIFT
import matplotlib.pyplot as plt
 
def view_key_points():
    img1 = rgb2gray(data.astronaut())
    img2 = transform.rotate(img1, 180)
    tform = transform.AffineTransform(scale=(1.3, 1.1), rotation=0.5, translation=(0, -200))
    img3 = transform.warp(img1, tform)

    descriptor_extractor = SIFT()

    descriptor_extractor.detect_and_extract(img1)
    keypoints1 = descriptor_extractor.keypoints
    descriptors1 = descriptor_extractor.descriptors

    descriptor_extractor.detect_and_extract(img2)
    keypoints2 = descriptor_extractor.keypoints
    descriptors2 = descriptor_extractor.descriptors

    descriptor_extractor.detect_and_extract(img3)
    keypoints3 = descriptor_extractor.keypoints
    descriptors3 = descriptor_extractor.descriptors

    matches12 = match_descriptors(
        descriptors1, descriptors2, max_ratio=0.6, cross_check=True
    )
    matches13 = match_descriptors(
        descriptors1, descriptors3, max_ratio=0.6, cross_check=True
    )
    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(11, 8))

    plt.gray()

    plot_matches(ax[0, 0], img1, img2, keypoints1, keypoints2, matches12)
    ax[0, 0].axis('off')
    ax[0, 0].set_title("Original Image vs. Flipped Image\n" "(all keypoints and matches)")

    plot_matches(ax[1, 0], img1, img3, keypoints1, keypoints3, matches13)
    ax[1, 0].axis('off')
    ax[1, 0].set_title(
        "Original Image vs. Transformed Image\n" "(all keypoints and matches)"
    )

    plot_matches(
        ax[0, 1], img1, img2, keypoints1, keypoints2, matches12[::15], only_matches=True
    )
    ax[0, 1].axis('off')
    ax[0, 1].set_title(
        "Original Image vs. Flipped Image\n" "(subset of matches for visibility)"
    )

    plot_matches(
        ax[1, 1], img1, img3, keypoints1, keypoints3, matches13[::15], only_matches=True
    )
    ax[1, 1].axis('off')
    ax[1, 1].set_title(
        "Original Image vs. Transformed Image\n" "(subset of matches for visibility)"
    )

    plt.tight_layout()
    plt.show()
    
#____________________________________________________________________
def plot_keypoints(image, keypoints):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(image, cmap='gray')
    
    for keypoint in keypoints:
        y, x = keypoint[0], keypoint[1]
        size = 1  
        circle = plt.Circle((x, y), size, color='g', fill=False, linewidth=1.5)
        ax.add_patch(circle)

    ax.set_title("Puntos clave extraídos con SIFT")
    ax.axis('off')
    plt.show()
    
