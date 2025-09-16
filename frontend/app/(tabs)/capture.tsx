import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image, Alert } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import { useRouter } from 'expo-router';

export default function CaptureScreen() {
  const [imageUri, setImageUri] = useState<string | null>(null);
  const router = useRouter();

  // Função para escolher imagem da galeria
  const pickImageFromGallery = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 1,
    });

    if (!result.canceled) {
      setImageUri(result.assets[0].uri);
    }
  };
  
  // Função para tirar foto com a câmera
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
  
  // Função para ir para a próxima tela
  const handleAnalysis = () => {
    if (imageUri) {
      Alert.alert("Próximo Passo", "Aqui nós navegaríamos para a tela de análise com a imagem selecionada.");
      // Futuramente: router.push({ pathname: '/analysis', params: { imageUri } });
    }
  }

  // Se nenhuma imagem foi escolhida, mostra os botões de seleção
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
  if (imageUri) {
    // Navega para a tela de análise passando a URI da imagem como parâmetro
    router.push({ pathname: '/analysis', params: { imageUri } });
  }
  // Se uma imagem foi escolhida, mostra a pré-visualização
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
    }
});