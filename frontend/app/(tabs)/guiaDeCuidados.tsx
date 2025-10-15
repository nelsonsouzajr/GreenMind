import { Text, View, StyleSheet } from 'react-native';

export default function GuiaDeCuidadosScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Guia de Cuidados</Text>
      <Text>Aqui ficará a enciclopédia de plantas.</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  title: { fontSize: 24, fontWeight: 'bold' },
});