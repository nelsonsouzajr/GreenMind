import React from 'react';
import { StyleSheet, Text, View, TouchableOpacity, StatusBar, Image } from 'react-native';
import { Link } from 'expo-router';

export default function HomeScreen() {
  return (
    <View style={styles.container}>
      <StatusBar barStyle="dark-content" />
      
      {/* A imagem da logo é chamada aqui com o caminho correto */}
      <Image 
        source={require('G:/Cursos/UNIVESP/2025-2/Projeto Integrador/GreenMind/frontend/assets/images/Logo.png')} 
        style={styles.logo} 
        resizeMode="contain"
      />

      <Text style={styles.title}>GreenMind</Text>
      
      <Text style={styles.subtitle}>
        Suas plantas pedem ajuda. Vamos descobrir o que elas têm?
      </Text>

      <Link href="/capture" asChild>
        <TouchableOpacity style={styles.button}>
          <Text style={styles.buttonText}>ANALISAR PLANTA</Text>
        </TouchableOpacity>
      </Link>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5ff',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  logo: {
    width: 150,
    height: 150,
    // resizeMode: 'contain', // <-- REMOVIDO DAQUI
    marginBottom: 20,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#2e7d32',
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
    paddingHorizontal: 60,
    borderRadius: 30,
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});