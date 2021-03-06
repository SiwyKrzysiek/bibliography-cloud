import React, { useState } from 'react';
import { Text, View, TextInput, Button, FlatList, StyleSheet } from 'react-native';

export default function PublicationsList({ publications, refreshPublications }) {

  const renderPublication = (publications) => {
    const selfLink = publication.links.find((l) => l.rel === 'self');
    const deleteLink = publication.links.find((l) => l.rel === 'delete');

    const deletePublication = async () => {
      await fetch(deleteLink.href, {
        method: 'DELETE',
      });
      refreshPublications();
    };

    return (
      <View style={{ flexDirection: "row" }}>
        <Text>{publication.title}</Text>
        {deleteLink &&
          <Button onPress={deletePublication}>Delete</Button>
        }
      </View>
    );
  }

  return (
    <View style={styles.container}>

      <FlatList
        data={publications}
        renderItem={({ item }) => <Text>{item.title}</Text>}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 10,
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});