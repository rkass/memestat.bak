#include <cv.h>
#include <highgui.h>
#include <sstream>
#include <dirent.h>

using namespace cv;

float avgDistance(vector <DMatch> dmatches, int n){

  float best[n];
  for (vector <DMatch>::size_type i = 0; i < dmatches.size(); i++){
    if (i < n)
      best[i] = dmatches[i].distance;
    else{
      for(int y = 0; y < n; y++){
        if(dmatches[i].distance < best[y]){
          float last = dmatches[i].distance;
          for(int x = y; x < n; x++){
            float tmp = last;
            last = best[x];
            best[x] = tmp;
          }   
          break;
        }
      }
    }
  }
  float total = 0;
  for (int i = 0; i < n; i++){
    total += best[i];
  }
  return total/n;
}

float avgDistance(vector <DMatch> dmatches){
  float dist = 0;
  for (vector <DMatch>::size_type i = 0; i < dmatches.size(); i++)
    dist += dmatches[i].distance;
  return (dist/dmatches.size());
}

vector<string> getDir(){
  vector<string> ret;
  DIR *dir;
  struct dirent *ent;
  string dirName = "/home/ryan/Dropbox/library";
  dir = opendir (dirName.c_str());
  while ((ent = readdir (dir)) != NULL){
    string file = ent -> d_name;
    //does it contain a leading "." ?
    if (file.compare(0, 1, ".")){
      string fullPath = dirName + "/" + file;
      ret.push_back(fullPath); 
    }
  }
  closedir(dir);
  return ret;
}

Mat indexToLib(int i){
  DIR *dir;
  struct dirent *ent;
  string dirName = "/home/ryan/Dropbox/library";
  dir = opendir (dirName.c_str());
  int x = 0;
  while ((ent = readdir (dir)) != NULL){
    string file = ent -> d_name;
    //does it contain a leading "." ?
    if (file.compare(0, 1, ".")){
      if (x == i){
        return imread(dirName + "/" + file, 1); 
      }
      x++; 
    }
  }
  return imread(dirName + "/" + "x", 1);
}

float getDiff(vector<float> x, vector<float> y){
  float ret = 0;
  for(int i = 0; i < x.size(); i++){
    float z = pow((x[i] - y[i]), 2);
    ret += z;
  }
  return ret;
}
  
float round(float r) {
    return (r > 0.0) ? floor(r + 0.5) : ceil(r - 0.5);
}

vector<float> assign(Mat img, int buckets, vector<KeyPoint> kp){
  vector<float> ret(buckets*3);
  int i = 0;  
  printf("kp size : %lu", kp.size());
  while(i < kp.size()){
    int x = kp[i].pt.x;
    int y = kp[i].pt.y;
    float fbuckets = buckets;
    float initRed = img.at<cv::Vec3b>(x,y)[0];
    float initGreen = img.at<cv::Vec3b>(x,y)[1];
    float initBlue = img.at<cv::Vec3b>(x,y)[2];
    float red = floor(initRed/255.0 * fbuckets);
    float green = floor(initGreen/255.0 * fbuckets) + 10;
    float blue = floor(initBlue/255.0 * fbuckets) + 20;
    int finalRed = min(fbuckets - 1, red);
    int finalGreen = min(fbuckets*2 - 1, green);
    int finalBlue = min(fbuckets*3 - 1, blue); 
    ret[finalRed] += 1;
    ret[finalGreen] += 1;
    ret[finalBlue] += 1; 
    i++;
  }
  float size;
  for(int i = 0; i < ret.size(); i++){
    size = img.rows * img.cols;
    ret[i] = ret[i] / size;
  }
  return ret;
}


vector<float> assign(Mat img, int buckets){
  vector<float> ret(buckets*3);
  for(int i = 0; i < img.rows; i++){
    for(int j = 0; j < img.cols; j++){
      float fbuckets = buckets;
      float initRed = img.at<cv::Vec3b>(i,j)[0];
      float initGreen = img.at<cv::Vec3b>(i,j)[1];
      float initBlue = img.at<cv::Vec3b>(i,j)[2];
      float red = floor(initRed/255.0 * fbuckets);
      float green = floor(initGreen/255.0 * fbuckets) + 10;
      float blue = floor(initBlue/255.0 * fbuckets) + 20;
      int finalRed = min(fbuckets - 1, red);
      int finalGreen = min(fbuckets*2 - 1, green);
      int finalBlue = min(fbuckets*3 - 1, blue);
     // printf("Red %d", finalRed);
     // printf("Green %d", finalGreen);
     // printf("Blue %d", finalBlue);
      ret[finalRed] += 1;
      ret[finalGreen] += 1;
      ret[finalBlue] += 1;
    }
  }
  float size;
  for(int i = 0; i < ret.size(); i++){
    size = img.rows * img.cols;
    ret[i] = ret[i] / size;
  }
  return ret;
}
     
Mat focus(Mat unfocusedImage){ 
     int y_offset= ((unfocusedImage.rows/2)- (unfocusedImage.rows/4)); 
     int x_offset = 0;
     Mat focusedImage = unfocusedImage(Rect(x_offset, y_offset, unfocusedImage.cols, unfocusedImage.rows/2));
     return focusedImage;
}


void verifyRead(Mat img, string s){
  if(!img.data){ 
    puts("Couldn't read image: ");
    puts(s.c_str());
    throw new String("Could not read image");
  }
}    
    
vector<Mat> stringToMats(vector<string> library){
  vector<Mat> ret(library.size());

  for(int i = 0; i < ret.size(); i++){
    ret[i] = imread(library[i], 1);
    verifyRead(ret[i], library[i]);
  }
  return ret;
}

Mat stringToMat(string target){
  Mat ret = imread(target, 1);
  verifyRead(ret, target);
  return ret;
}
 
int pixelBuckets(int argc, char** argv, int buckets){
  vector<string> library = getDir();
  vector<Mat> lib = stringToMats(library);
  Mat targ = stringToMat(argv[1]);
  vector <vector<float> > libAssignments(lib.size());
  Ptr <FeatureDetector> fast;
  fast = FeatureDetector::create("FAST");
  vector <vector <KeyPoint> > libraryKps;
  fast -> detect(lib, libraryKps);
  vector <KeyPoint> targkps;
  fast -> detect(targ, targkps);
  for(int i = 0; i < libAssignments.size(); i++)
    libAssignments[i] = assign(lib[i], buckets, targkps);
  vector <float> targAssignment = assign(targ, buckets, targkps);
  float secondBest = 100;
  float bestMatch = 100;
  int minIndex = 0;
  int secondMin = 0;
  for(int i = 0; i < libAssignments.size(); i++){
    if(targAssignment.size() != libAssignments[i].size())
      printf("Shits fucked");

    float diff = getDiff(targAssignment, libAssignments[i]);
    if (diff < bestMatch){
      secondBest = bestMatch;
      bestMatch = diff;
      secondMin = minIndex;
      minIndex = i;
    }
    else if(diff < secondBest){
      secondBest = diff;
      secondMin = i;
    }
  }
  printf("Second Best Match: %s\nScore: %f\n", library[secondMin].c_str(), secondBest);
  printf("Best Match: %s\nScore: %f\n", library[minIndex].c_str(), bestMatch);
  return 1;
}
  
int descriptorMatch(int argc, char** argv){
  //get images
  vector<Mat> libraryImages = stringToMats(getDir());
  Mat targetImage = stringToMat(argv[1]);
  
  //keypoint initialization
  vector <vector <KeyPoint> > libraryKps;
  vector <KeyPoint> targetKps;
  
  //descriptors initialization  
  vector <Mat> libraryDescriptors;
  Mat targetDescriptors;
  
  //descriptor matches initializtion
  vector <vector <DMatch> > matches;
   
  //initialize computation pointers
  Ptr <FeatureDetector> featureDetector;
  Ptr <DescriptorExtractor> descriptorExtractor;
  Ptr <DescriptorMatcher> descriptorMatcher;
  featureDetector = FeatureDetector::create("FAST");
  descriptorExtractor = DescriptorExtractor::create("FREAK");
  descriptorMatcher = DescriptorMatcher::create("BruteForce");
  
  //Detect keypoints
  featureDetector -> detect(libraryImages, libraryKps);
  featureDetector -> detect(targetImage, targetKps);
  
  //Compute Descriptors for library, then target
  descriptorExtractor -> compute(libraryImages, libraryKps, libraryDescriptors);
  descriptorExtractor -> compute(targetImage, targetKps, targetDescriptors);
  descriptorMatcher -> add(libraryDescriptors);
  vector <DMatch> matches2;
  descriptorMatcher -> match(targetDescriptors, matches2);
  vector<int> bestMatch(matches2.size());
  for (vector <DMatch>::size_type i = 0; i < matches2.size(); i++){
    //printf("Query Index: %d\n", matches2[i].queryIdx);
    //printf("Train Index: %d\n", matches2[i].trainIdx);
    //printf("Image Index: %d\n", matches2[i].imgIdx);
    bestMatch[matches2[i].imgIdx] += 1;
  }
  int max = 0;
  int maxIndex = 0;
  for (int i = 0; i < bestMatch.size(); i++){
    if (bestMatch[i] > max){
      max = bestMatch[i];
      maxIndex = i;
    }
  }
  //match keypoints on target image to each library image and draw
  /*for (int i = 0; i < libraryDescriptors.size(); i++){
    puts("here");
    descriptorMatcher -> match(targetDescriptors, libraryDescriptors[i], matches[i]);
    puts("herend");
    printf("%d: %f \n", i, avgDistance(matches[i]));
  }*/
  //descriptorMatcher -> match(targetDescriptors, matches, libraryDescriptors);
 printf("Max Matches: %d", max);
  namedWindow( "Display window", CV_WINDOW_AUTOSIZE );// Create a window for display.
  imshow( "Display window", indexToLib(maxIndex));                   // Show our image inside it.

    waitKey(0);           
  return 0;
}

/*options: 
  pixelBuckets (takes additional argument buckets)
    Looks at each pixel's RGB values and classify each into one of n buckets.
    Compare differences in size of each image's total buckets.
  descriptorMatch
    Tries to find the image with the minimum distance between descriptors.
*/

int main (int argc, char** argv){
  //return pixelBuckets(argc, argv, 5);
  return descriptorMatch(argc, argv);
}

