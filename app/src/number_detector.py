import os
import sys
from threading import Lock
import numpy as np
import warnings
from typing import Optional

warnings.filterwarnings('ignore')

# packages will be availables inside DOcker container

lock = Lock()

# NomeroffNet path
NOMEROFF_NET_DIR = os.path.abspath('/app/nomeroff-net')
sys.path.append(NOMEROFF_NET_DIR)
# Import license plate recognition tools.
from NomeroffNet.YoloV5Detector import Detector
detector = Detector()
detector.load()

from NomeroffNet.BBoxNpPoints import NpPointsCraft, getCvZoneRGB, convertCvZonesRGBtoBGR, reshapePoints
npPointsCraft = NpPointsCraft()
npPointsCraft.load()

from NomeroffNet.OptionsDetector import OptionsDetector
from NomeroffNet.TextDetector import TextDetector

from NomeroffNet import TextDetector
from NomeroffNet import textPostprocessing

# load models
optionsDetector = OptionsDetector()
optionsDetector.load("latest")

textDetector = TextDetector.get_static_module("eu")
textDetector.load("latest")

def detect(img: np.ndarray) -> Optional[str]:

    # Ensure that only one model is loaded among all threads.
    with lock:
      targetBoxes = detector.detect_bbox(img)
      all_points = npPointsCraft.detect(img, targetBoxes,[5,2,0])

      # cut zones
      zones = convertCvZonesRGBtoBGR([getCvZoneRGB(img, reshapePoints(rect, 1)) for rect in all_points])

      # predict zones attributes
      regionIds, stateIds = optionsDetector.predict(zones)
      regionNames = optionsDetector.getRegionLabels(regionIds)

      # find text with postprocessing by standart
      textArr = textDetector.predict(zones)
      textArr = textPostprocessing(textArr, regionNames)

    return textArr[0] if textArr else None