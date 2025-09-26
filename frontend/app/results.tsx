import { View, Text, StyleSheet, Image, ScrollView, TouchableOpacity } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import React from 'react';

// Definimos um tipo para a nossa previsão para maior segurança do código
type Prediction = {
  prediction: string;
  confidence: string;
};

export default function ResultsScreen() {
  const { results: resultsString, imageUri } = useLocalSearchParams<{ results: string, imageUri: string }>();
  const router = useRouter();

  // 1. Convertemos a string JSON de volta para um array de objetos
  const predictions: Prediction[] = resultsString ? JSON.parse(resultsString) : [];
  
  // Pegamos a primeira previsão (a mais provável) para destacar
  const topPrediction = predictions[0];

  return (
    <ScrollView contentContainerStyle={styles.container}>
      {imageUri && <Image source={{ uri: imageUri }} style={styles.image} />}
      
      <Text style={styles.title}>Resultado da Análise</Text>

      {/* Card para a previsão principal */}
      {topPrediction && (
        <View style={styles.card}>
          <Text style={styles.cardTitle}>Diagnóstico Principal</Text>
          <Text style={styles.predictionText}>{topPrediction.prediction}</Text>
          <Text style={styles.confidenceText}>Confiança: {topPrediction.confidence}</Text>
        </View>
      )}

      {/* Card para outras possibilidades */}
      {predictions.length > 1 && (
        <View style={styles.card}>
          <Text style={styles.cardTitle}>Outras Possibilidades</Text>
          {predictions.slice(1).map((item, index) => (
            <View key={index} style={styles.otherPossibility}>
              <Text style={styles.cardContent}>{item.prediction}</Text>
              <Text style={styles.confidenceText}>{item.confidence}</Text>
            </View>
          ))}
        </View>
      )}

      <TouchableOpacity style={styles.button} onPress={() => router.push('/')}>
        <Text style={styles.buttonText}>Analisar Outra Planta</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
    container: {
        padding: 20,
        backgroundColor: '#f5f5f5',
    },
    image: {
        width: '100%',
        height: 250,
        borderRadius: 10,
        marginBottom: 20,
        resizeMode: 'cover',
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#333',
        marginBottom: 20,
        textAlign: 'center',
    },
    card: {
        backgroundColor: '#fff',
        borderRadius: 8,
        padding: 15,
        marginBottom: 15,
        elevation: 2,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 1 },
        shadowOpacity: 0.22,
        shadowRadius: 2.22,
    },
    cardTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        color: '#2e7d32',
        marginBottom: 10,
    },
    cardContent: {
        fontSize: 16,
        color: '#616161',
    },
    predictionText: {
        fontSize: 18,
        fontWeight: 'bold',
        color: '#000',
        marginBottom: 5,
    },
    confidenceText: {
        fontSize: 14,
        color: '#888',
    },
    otherPossibility: {
        marginBottom: 10,
    },
    button: {
      backgroundColor: '#4caf50',
      paddingVertical: 15,
      borderRadius: 30,
      alignItems: 'center',
      marginTop: 20,
    },
    buttonText: {
      color: '#fff',
      fontSize: 16,
      fontWeight: 'bold',
    },
});