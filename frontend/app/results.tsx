import { View, Text, StyleSheet, Image, ScrollView, TouchableOpacity } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import React from 'react';

export default function ResultsScreen() {
  const { imageUri } = useLocalSearchParams<{ imageUri: string }>();
  const router = useRouter();

  // Dados de exemplo (mock)
  const analysisResult = {
    plantName: 'Samambaia (Nephrolepis exaltata)',
    healthDiagnosis: 'Saudável com leves sinais de desidratação.',
    careSuggestions: [
      'Regue de 2 a 3 vezes por semana, mantendo o solo úmido, mas não encharcado.',
      'Mantenha em um local com luz indireta. A luz solar direta pode queimar as folhas.',
      'Borrife água nas folhas periodicamente para aumentar a umidade.',
    ]
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      {imageUri && <Image source={{ uri: imageUri }} style={styles.image} />}
      
      <Text style={styles.title}>Resultado da Análise</Text>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Espécie Identificada</Text>
        <Text style={styles.cardContent}>{analysisResult.plantName}</Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Diagnóstico de Saúde</Text>
        <Text style={styles.cardContent}>{analysisResult.healthDiagnosis}</Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Sugestões de Cuidado</Text>
        {analysisResult.careSuggestions.map((suggestion, index) => (
          <Text key={index} style={styles.suggestionItem}>• {suggestion}</Text>
        ))}
      </View>

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
        elevation: 2, // Sombra para Android
        shadowColor: '#000', // Sombra para iOS
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
    suggestionItem: {
        fontSize: 16,
        color: '#616161',
        marginBottom: 5,
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