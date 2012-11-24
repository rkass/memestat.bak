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
  vector<string> ret(100);
  DIR *dir;
  struct dirent *ent;
  dir = opendir ("/home/ryan/Dropbox/library");
  int i = 0;
  while ((ent = readdir (dir)) != NULL){
    ret[i] = ent -> d_name;
    i++;
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
  

vector<float> assign(Mat img){
  vector<float> ret(15);
  for(int x = 0; x < 15; x++){
    ret[x] = 0;
  }
  for(int i = 0; i < img.rows; i++){
    for(int j = 0; j < img.cols; j++){
      if(img.at<cv::Vec3b>(i,j)[0] < 51)
        ret[0] += 1;
      else if(img.at<cv::Vec3b>(i,j)[0] < 102)
        ret[1] += 1;
      else if(img.at<cv::Vec3b>(i,j)[0] < 153)
        ret[2] += 1;
      else if(img.at<cv::Vec3b>(i,j)[0] < 204)
        ret[3] += 1;
      else
        ret[4] += 1;
      if(img.at<cv::Vec3b>(i,j)[1] < 51)
        ret[5] += 1;
      else if(img.at<cv::Vec3b>(i,j)[1] < 102)
        ret[6] += 1;
      else if(img.at<cv::Vec3b>(i,j)[1] < 153)
        ret[7] += 1;
      else if(img.at<cv::Vec3b>(i,j)[1] < 204)
        ret[8] += 1;
      else
        ret[9] += 1;
      if(img.at<cv::Vec3b>(i,j)[2] < 51)
        ret[10] += 1;
      else if(img.at<cv::Vec3b>(i,j)[2] < 102)
        ret[11] += 1;
      else if(img.at<cv::Vec3b>(i,j)[2] < 153)
        ret[12] += 1;
      else if(img.at<cv::Vec3b>(i,j)[2] < 204)
        ret[13] += 1;
      else
        ret[14] += 1;
    }
  }
  float size;
  for(int i = 0; i < ret.size(); i++){
    size = img.rows * img.cols;
    ret[i] = ret[i] / size;
  }
  return ret;

}
            
int pixelBuckets(vector<string> library, string target){
  vector<Mat> lib(library.size());
  for(int i = 0; i < lib.size(); i++)
    lib[i] = imread(library[i], 1);
  Mat targ = imread(target, 1);
  vector <vector<float> > libAssignments(lib.size());
  for(int i = 0; i < libAssignments.size(); i++)
    libAssignments[i] = assign(lib[i]);
  vector <float> targAssignment = assign(targ);
  float bestMatch = 100;
  int minIndex = 0;
  for(int i = 0; i < libAssignments.size(); i++){
    float diff = getDiff(targAssignment, libAssignments[i]);
    printf("%s Match: %f: \n", library[i].c_str(), diff);
    if (diff < bestMatch){
      bestMatch = diff;
      minIndex = i;
    }
  }
  printf("Best Match: %s\nScore: %f\n", library[minIndex].c_str(), bestMatch);
  return 1;
}
  


int main (int argc, char** argv){
  vector<string> lib = getDir();
  int size = 0;
  for(int i = 0; i < lib.size(); i++){
    if (lib[i].find(".jpg") != string::npos)
      size++;
  }
  vector<string> library(size);
  int x = 0;
  for(int i = 0; i < lib.size(); i++){
    if (lib[i].find(".jpg") != string::npos){
       library[x] = "/home/ryan/Dropbox/library/" + lib[i];
       x++;
    }
  }
  return pixelBuckets(library, argv[1]);/*

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
