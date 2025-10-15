import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image, Alert, ActivityIndicator } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import { useRouter } from 'expo-router';
// 1. IMPORTAR FileSystem da sua nova localização "legacy"
import { readAsStringAsync, EncodingType } from 'expo-file-system/legacy';

// IMPORTANT: Replace with your computer's local IP address.
const API_URL = 'http://192.168.15.113:5000/predict';

export default function CaptureScreen() {
  const [imageUri, setImageUri] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const pickImageFromGallery = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: false, // Alterado para false
      quality: 1,
    });

    if (!result.canceled) {
      setImageUri(result.assets[0].uri);
    }
  };

  const pickImageFromCamera = async () => {
    const permissionResult = await ImagePicker.requestCameraPermissionsAsync();
    if (permissionResult.granted === false) {
      Alert.alert("Permissão necessária", "Você precisa permitir o acesso à câmera para tirar uma foto.");
      return;
    }

    let result = await ImagePicker.launchCameraAsync({
      allowsEditing: true,
      aspect: [4, 3],
      quality: 1,
    });

    if (!result.canceled) {
      setImageUri(result.assets[0].uri);
    }
  };

  const handleAnalysis = async () => {
    console.log("Botão clicado! A função handleAnalysis começou.");
    if (!imageUri) return;

    setIsLoading(true);

    try {
      // 2. Usar as funções e tipos importados corretamente
      const base64Image = await readAsStringAsync(imageUri, {
        encoding: EncodingType.Base64,
      });

      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: base64Image }),
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.error || 'Erro na API');
      }

      router.push({
        pathname: '/results',
        params: { results: JSON.stringify(result), imageUri: imageUri },
      });

    } catch (error) {
      console.error(error);
      Alert.alert("Erro", "Não foi possível conectar ao servidor de análise. Verifique se o servidor está rodando e o IP está correto.");
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
        <View style={[styles.container, styles.loadingContainer]}>
            <ActivityIndicator size="large" color="#4caf50" />
            <Text style={styles.loadingText}>Analisando sua planta...</Text>
        </View>
    );
  }

  if (!imageUri) {
    return (
      <View style={styles.container}>
        <Text style={styles.title}>Selecione uma Imagem</Text>
        <Text style={styles.subtitle}>
          Tire uma foto da planta ou escolha uma imagem da sua galeria.
        </Text>
        <TouchableOpacity style={styles.button} onPress={pickImageFromCamera}>
          <Text style={styles.buttonText}>Tirar Foto com a Câmera</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.button} onPress={pickImageFromGallery}>
          <Text style={styles.buttonText}>Escolher da Galeria</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Imagem Selecionada</Text>
      <Image source={{ uri: imageUri }} style={styles.previewImage} />
      <TouchableOpacity style={styles.button} onPress={handleAnalysis}>
        <Text style={styles.buttonText}>Analisar Imagem</Text>
      </TouchableOpacity>
      <TouchableOpacity style={[styles.button, styles.buttonSecondary]} onPress={() => setImageUri(null)}>
        <Text style={[styles.buttonText, styles.buttonTextSecondary]}>Escolher Outra</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: '#f5f5f5',
      alignItems: 'center',
      justifyContent: 'center',
      padding: 20,
    },
    title: {
      fontSize: 24,
      fontWeight: 'bold',
      color: '#333',
      marginBottom: 10,
    },
    subtitle: {
      fontSize: 16,
      color: '#616161',
      textAlign: 'center',
      marginBottom: 40,
    },
    button: {
      backgroundColor: '#4caf50',
      paddingVertical: 15,
      paddingHorizontal: 40,
      borderRadius: 30,
      marginBottom: 15,
      width: '80%',
      alignItems: 'center',
    },
    buttonText: {
      color: '#fff',
      fontSize: 16,
      fontWeight: 'bold',
    },
    buttonSecondary: {
        backgroundColor: 'transparent',
        borderWidth: 2,
        borderColor: '#4caf50',
    },
    buttonTextSecondary: {
        color: '#4caf50',
    },
    previewImage: {
      width: 300,
      height: 300,
      resizeMode: 'contain',
      marginBottom: 20,
      borderRadius: 10,
    },
    loadingContainer: {
        justifyContent: 'center',
    },
    loadingText: {
        marginTop: 20,
        fontSize: 18,
        fontWeight: 'bold',
        color: '#333',
    }
});