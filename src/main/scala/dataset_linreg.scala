import org.apache.spark.ml.Pipeline
import org.apache.spark.ml.classification.LogisticRegression
import org.apache.spark.sql.functions.broadcast
import org.apache.spark.sql.{Column, ColumnName, DataFrame, Dataset, SparkSession}

import scala.collection.mutable
import org.apache.spark.ml.feature.{Bucketizer, LabeledPoint, StringIndexer, VectorAssembler}

import org.apache.spark.ml.evaluation.RegressionEvaluator



object Main {

    def main(args: Array[String]): Unit = {

      val spark = SparkSession.builder().master("local[*]").appName("First spark app").getOrCreate()

      import spark.implicits._
      import org.apache.spark.sql.functions._
      import org.apache.spark.broadcast._
      import org.apache.spark.sql.types._
      import spark.sparkContext.broadcast

      // "facebook_checkins", "facebook_rating", "favorites_count_KudaGo", events_count_KudaGo, comments_count_KudaGo, foursquare_checkinsCount, foursquare_rating, foursquare_ratingVotes, foursquare_userCount, instagram_visitorsNumber

// самые часто встречаемые бренды
      var city_brands : DataFrame= spark.read.parquet("merged_spb.parquet")
              .groupBy("city_brand")
              .agg(count("city_brand"))
              .sort($"count(city_brand)".desc)


        //самые часто встречаемые категории
      var categories : DataFrame= spark.read.parquet("merged_spb.parquet")
              .groupBy("categories")
              .agg(count("categories"))
              .sort($"count(categories)".desc)
              .limit(6)

        // рейтинги по каждому источнику по всем категориям
      var tripadvisor_rating : DataFrame = spark.read.parquet("merged_spb.parquet")
        .filter($"tripAdvisor_reviewsNumber".isNotNull)
        .select("title","additional_categories", "address", "categories", "city_brand", "tripAdvisor_rating","tripAdvisor_reviewsNumber" , "wikipedia_title")
        .sort($"tripAdvisor_reviewsNumber".desc)

      var facebook_rating : DataFrame = spark.read.parquet("merged_spb.parquet")
        .filter($"facebook_checkins".isNotNull)
        .select("title","additional_categories", "address", "categories", "city_brand", "facebook_checkins","facebook_rating" , "wikipedia_title")
        .sort($"facebook_checkins".desc)

      var kudago_rating : DataFrame = spark.read.parquet("merged_spb.parquet")
        .filter($"favorites_count_KudaGo".isNotNull)
        .select("title","additional_categories", "address", "categories", "city_brand", "favorites_count_KudaGo","events_count_KudaGo" ,"comments_count_KudaGo", "wikipedia_title")
        .sort($"favorites_count_KudaGo".desc)


      var instagram_rating : DataFrame = spark.read.parquet("merged_spb.parquet")
        .filter($"instagram_visitorsNumber".isNotNull)
        .select("title","additional_categories", "address", "categories", "city_brand", "instagram_visitorsNumber", "wikipedia_title")
        .sort($"instagram_visitorsNumber".desc)

      var foursquare_rating : DataFrame = spark.read.parquet("merged_spb.parquet")
        .filter($"foursquare_checkinsCount".isNotNull)
        .select("title","additional_categories", "address", "categories", "city_brand", "foursquare_userCount","foursquare_rating","foursquare_ratingVotes","foursquare_checkinsCount","wikipedia_title")
        .sort($"foursquare_checkinsCount".desc)


      // самые популярные бренды спб
      var rating_city_brand : DataFrame = tripadvisor_rating
        .groupBy("city_brand")
        .agg(sum("tripAdvisor_reviewsNumber"))
        .sort($"sum(tripAdvisor_reviewsNumber)".desc)


      var categor = Seq(Array("Restaurant"), Array("Sights & Landmarks"), Array("Nature & Parks"), Array("Museums & Libraries"), Array("Concerts & Shows")).toList

        // самые популярные заведения по категорям согласно фейсбуку
      def sortByCategorFacebook (categoria : Array[String]) : DataFrame = {
        facebook_rating
          .filter($"categories" === categoria)
          .sort($"facebook_checkins".desc)
      }

      for (i <- categor) sortByCategorFacebook(i)





      /////// work with google-data


      val df = spark.read
        .format("com.databricks.spark.csv")
        .option("header", "true")
        .option("delimiter", ",")
        .option("inferSchema", "false")
        .load("cafe_prep.csv")

// change categorical variables
      val indexer = new StringIndexer()
        .setInputCol("types")
        .setOutputCol("indexed_types")
        .fit(df)

      val indexer2 = new StringIndexer()
        .setInputCol("closest_metro")
        .setOutputCol("indexed_metro")
        .fit(df)

      var df1 = indexer.transform(df)
      var df2 = indexer2.transform(df1)

      var df3 = df2.drop("types", "closest_metro").withColumnRenamed("user_ratings_total", "label")

      import org.apache.spark.sql.types
      var df4 = df3.select(df3.columns.map(c => col(c).cast(DoubleType)) : _*)
          .na.drop()


      df4.printSchema()



      import org.apache.spark.mllib.linalg.Vectors

      import org.apache.spark.ml.regression.GeneralizedLinearRegression

      val splits = df4.randomSplit(Array(0.6, 0.4), seed = 11L)
      val train = splits(0).cache()
      val test = splits(1)



      val assembler = new VectorAssembler()
        .setInputCols(Array("_c0", "price_level", "rating", "lat", "lng", "closest_metro_km", "Quantity of nearest museum", "Quantity of nearest art_gallery", "Quantity of nearest shopping_mall", "Quantity of nearest places_tourist_attraction", "Quantity of nearest same establishment", "opportunity_take_away", "distance_to_center, km", "indexed_types", "indexed_metro"))
        .setOutputCol("features")

      val lr = new GeneralizedLinearRegression()
        .setMaxIter(10)
        .setRegParam(0.3)
        //.setElasticNetParam(0.8)
        .setFeaturesCol("features")   // setting features column
        .setLabelCol("label")



      // Fit the model
      val model = lr.fit(assembler.transform(train))

      val prediction = model.transform(assembler.transform(test))


      // Print the coefficients and intercept for generalized linear regression model
      println(s"Coefficients: ${model.coefficients}")
      println(s"Intercept: ${model.intercept}")


      val evaluator = new RegressionEvaluator()
        .setLabelCol("label")
        .setPredictionCol("prediction")
        .setMetricName("rmse")

      println("rmse = ", evaluator.evaluate(prediction))

    }
}



