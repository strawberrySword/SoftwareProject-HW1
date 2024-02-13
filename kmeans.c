#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define EPSILON 0.001

typedef struct
{
   int size;
   float *center;
   float *currentCenter;
} Centroid;

int findClosestCluster(float[], Centroid[], int, int);
float CalcEclideanDistance(float[], float[], int);

float CalcEclideanDistance(float u[], float v[], int d)
{
   float squareSum;
   int i;
   squareSum = 0;
   for (i = 0; i < d; i++)
   {
      squareSum += (u[i] - v[i]) * (u[i] - v[i]);
   }

   return sqrt(squareSum);
}

int findClosestCluster(float dataPoint[], Centroid centroids[], int d, int k)
{
   int closest, i;
   float minDistance, distance;
   closest = 0;
   minDistance = CalcEclideanDistance(dataPoint, centroids[0].center, d);

   for (i = 0; i < k; i++)
   {
      distance = CalcEclideanDistance(dataPoint, centroids[i].center, d);
      if (distance < minDistance)
      {
         minDistance = distance;
         closest = i;
      }
   }
   return closest;
}

int main(int argc, char *argv[])
{
   /* declerations */
   int i, j, l, n, k, d, iter, closest;
   float current, maxDelta, delta;
   Centroid *centroids;
   float **dataPoints;
   printf("%d\n", argc);
   /* parsing parameters */
   k = atoi(argv[1]);
   n = atoi(argv[2]);
   d = atoi(argv[3]);
   iter = atoi(argv[4]);

   /* allocation */

   centroids = calloc(k, sizeof(Centroid));
   dataPoints = (float **)calloc(n, sizeof(float *));

   for (i = 0; i < n; i++)
   {
      dataPoints[i] = (float *)calloc(d, sizeof(float));
   }

   /* parsing the input */
   for (i = 0; i < n; i++)
   {
      for (j = 0; (j < d) && (scanf("%f,", &current) != EOF); j++)
      {
         dataPoints[i][j] = current;
      }
   }

   /* initialization and centroids allocation */
   for (i = 0; i < k; i++)
   {
      centroids[i].size = 0;
      centroids[i].center = (float *)calloc(d, sizeof(float));
      centroids[i].currentCenter = (float *)calloc(d, sizeof(float));

      for (j = 0; j < d; j++)
      {
         centroids[i].center[j] = dataPoints[i][j];
         centroids[i].currentCenter[j] = 0;
      }
   }

   /* main loop */
   maxDelta = 1 + EPSILON;
   for (i = 0; (i < iter) && (maxDelta > EPSILON); i++)
   {
      /* find closest cluster for every x in dataPoints */
      for (j = 0; j < n; j++)
      {
         closest = findClosestCluster(dataPoints[j], centroids, d, k);
         centroids[closest].size += 1;
         for (l = 0; l < d; l++)
         {
            centroids[closest].currentCenter[l] = centroids[closest].currentCenter[l] + dataPoints[j][l];
         }
      }

      /* recenter all clusters and update maxDelta */
      maxDelta = 0;
      for (j = 0; j < k; j++)
      {
         for (l = 0; l < d; l++)
         {
            centroids[j].currentCenter[l] = (centroids[j].currentCenter[l]) / (centroids[j].size);
         }
         delta = CalcEclideanDistance(centroids[j].currentCenter, centroids[j].center, d);
         if (delta > maxDelta)
         {
            maxDelta = delta;
         }

         for (l = 0; l < d; l++)
         {
            centroids[j].center[l] = centroids[j].currentCenter[l];
            centroids[j].currentCenter[l] = 0;
            centroids[j].size = 0;
         }
      }
   }

   /* print out the centrouds */
   for (i = 0; i < k; i++)
   {
      for (j = 0; j < d; j++)
      {
         printf("%.4f,", centroids[i].center[j]);
      }
      printf("\n");
   }

   /* free all allocated space */
   for (i = 0; i < k; i++)
   {
      free(centroids[i].center);
      free(centroids[i].currentCenter);
   }
   free(centroids);

   for (i = 0; i < n; i++)
   {
      free(dataPoints[i]);
   }
   free(dataPoints);
   return 0;
}