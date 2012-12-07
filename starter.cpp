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
     int y_offset= ((unfocusedImage.rows/2)-10); 
     int x_offset ((unfocusedImage.cols/2)-10);
     Mat focusedImage = unfocusedImage(Rect(x_offset, 30, 20,20));
     return focusedImage;
}


void verifyRead(Mat img, string s){
  if(!img.data){ 
    puts("Couldn't read image: ");
    puts(s.c_str());
    throw new String("Could not read image");
  }
}    
    
 
int pixelBuckets(vector<string> library, string target, int buckets){
  vector<Mat> lib(library.size());
  for(int i = 0; i < lib.size(); i++){
    lib[i] = focus(imread(library[i], 1));
    verifyRead(lib[i], library[i]);
    
  }
  Mat targ = focus(imread(target, 1));
  verifyRead(targ, target);
  vector <vector<float> > libAssignments(lib.size());
  for(int i = 0; i < libAssignments.size(); i++){
    libAssignments[i] = assign(lib[i], buckets);
  }
  vector <float> targAssignment = assign(targ, buckets);
  float secondBest = 100;
  float bestMatch = 100;
  int minIndex = 0;
  int secondMin = 0;
  for(int i = 0; i < libAssignments.size(); i++){
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
  //  if (library[i].compare(, target.size(), target))
    //  printf("Target Assignment: %s\nScore: %f\n", library[i].c_str(), diff);
      

  }
  printf("Second Best Match: %s\nScore: %f\n", library[secondMin].c_str(), secondBest);
  printf("Best Match: %s\nScore: %f\n", library[minIndex].c_str(), bestMatch);
  return 1;
}
  


int main (int argc, char** argv){
  vector<string> lib = getDir();
//  int size = 0;
 // for(int i = 0; i < lib.size(); i++){
   // if (lib[i].find(".jpg") != string::npos)
     // size++;
 // }
//  vector<string> library(size);
 // int x = 0;
 /* for(int i = 0; i < lib.size(); i++){
    if (lib[i].find(".jpg") != string::npos){
       library[x] = "/home/ryan/Dropbox/library/" + lib[i];
       x++;
    }
  }*/
  return pixelBuckets(lib, argv[1], 10);/*

  Mat i1, i2, target, freakOut1, freakOut2, targetFreakOut, kpsImg, matchImg1, matchImg2;
  i1 = imread (argv[1], 1);
  i2 = imread (argv[2], 1);
  target = imread (argv[3], 1);
  if (!i1.data){
      printf ("No image data \n");
      return -1;
  }
  vector <vector <KeyPoint> > libraryKps;
  vector <Mat> freakOuts;
  Mat ff[2] = {freakOut1, freakOut2};
  freakOuts.assign(&ff[0], &ff[0]+2);
  Mat vv[2] = {i1, i2};
  vector <Mat> library;
  library.assign(&vv[0], &vv[0]+2);
  Ptr <FeatureDetector> fast;
  Ptr <DescriptorExtractor> freakdes;
  Ptr <DescriptorMatcher> bfMatcher;
  fast = FeatureDetector::create("FAST");
  
  //Detect keypoints for library images
  fast -> detect(library, libraryKps);
  freakdes = DescriptorExtractor::create("FAST");
  //Compute Descriptors for each library image
  for (vector <vector <KeyPoint> >::size_type i = 0; i < libraryKps.size(); i++){
    freakdes -> compute(library[i], libraryKps[i], freakOuts[i]);
  }
  //Detect keypoints for target image
  vector <KeyPoint> targetKps;
  fast -> detect(target, targetKps);
  //Compute Descriptors for target image
  freakdes -> compute(target, targetKps, targetFreakOut);
  vector <DMatch> m1;
  vector <DMatch> m2;
  vector <vector <DMatch> > matches;
  vector <DMatch> dd[2] = {m1, m2};
  matches.assign(&dd[0], &dd[0]+2);
  bfMatcher = DescriptorMatcher::create("BruteForce");
  //match keypoints on target image to each library image and draw
  for (vector <vector <DMatch> >::size_type i = 0; i < matches.size(); i++){
    bfMatcher -> match(targetFreakOut, freakOuts[i], matches[i]);
    Mat tmp;
    drawMatches(target, targetKps, library[i], libraryKps[i], matches[i], tmp, Scalar(100, 100, 100));
    string s;
    std::stringstream out;
    out << i;
    s = out.str();
    imshow("Matches between target and library image " + s, tmp);
    printf("%lu: %f \n", i, avgDistance(matches[i], 5));
  }
  
  
  waitKey(0);
  return 0;*/
}
