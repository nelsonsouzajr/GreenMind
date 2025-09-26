import { View, Text, StyleSheet, ActivityIndicator } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import React, { useEffect } from 'react';

export default function AnalysisScreen() {
  const { imageUri } = useLocalSearchParams<{ imageUri: string }>();
  const router = useRouter();

  useEffect(() => {
    // Simula um tempo de análise de 3 segundos
    const timer = setTimeout(() => {
      if (imageUri) {
        // Navega para a tela de resultados, passando a imagem
        router.replace({ pathname: '/results', params: { imageUri } });
      }
    }, 3000);

    // Limpa o timer se o componente for desmontado
    return () => clearTimeout(timer);
  }, [imageUri]);

  return (
    <View style={styles.container}>
      <ActivityIndicator size="large" color="#4caf50" />
      <Text style={styles.text}>Analisando sua planta...</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    alignItems: 'center',
    justifyContent: 'center',
  },
  text: {
    marginTop: 20,
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
});