/**
 * Scanner Overlay Component
 * Overlay visual para o scanner com animações
 */

import React from 'react';
import {
  View,
  StyleSheet,
  Dimensions,
  Animated,
} from 'react-native';
import {colors, spacing} from '../../styles';

const {width, height} = Dimensions.get('window');

const ScannerOverlay = ({scanLineAnim, pulseAnim, isProcessing}) => {
  // Dimensões da área de scan
  const scanAreaSize = width * 0.7;
  const scanAreaTop = (height - scanAreaSize) / 2;
  const scanAreaLeft = (width - scanAreaSize) / 2;

  // Animação da linha de scan
  const scanLineTranslateY = scanLineAnim.interpolate({
    inputRange: [0, 1],
    outputRange: [0, scanAreaSize - 4],
  });

  return (
    <View style={styles.overlay}>
      {/* Overlay escuro */}
      <View style={styles.overlayTop} />
      <View style={styles.overlayMiddle}>
        <View style={styles.overlayLeft} />
        <View style={styles.scanArea} />
        <View style={styles.overlayRight} />
      </View>
      <View style={styles.overlayBottom} />

      {/* Área de scan */}
      <View
        style={[
          styles.scanFrame,
          {
            top: scanAreaTop,
            left: scanAreaLeft,
            width: scanAreaSize,
            height: scanAreaSize,
          },
        ]}>
        
        {/* Cantos do frame */}
        <View style={[styles.corner, styles.cornerTopLeft]} />
        <View style={[styles.corner, styles.cornerTopRight]} />
        <View style={[styles.corner, styles.cornerBottomLeft]} />
        <View style={[styles.corner, styles.cornerBottomRight]} />

        {/* Linha de scan animada */}
        {!isProcessing && (
          <Animated.View
            style={[
              styles.scanLine,
              {
                transform: [{translateY: scanLineTranslateY}],
              },
            ]}
          />
        )}

        {/* Efeito de pulso quando processando */}
        {isProcessing && (
          <Animated.View
            style={[
              styles.pulseEffect,
              {
                transform: [{scale: pulseAnim}],
              },
            ]}
          />
        )}
      </View>

      {/* Indicadores de status */}
      <View style={styles.statusIndicator}>
        <View
          style={[
            styles.statusDot,
            {
              backgroundColor: isProcessing
                ? colors.primary.green
                : colors.white,
            },
          ]}
        />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  overlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
  },
  overlayTop: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.6)',
  },
  overlayMiddle: {
    flexDirection: 'row',
    height: width * 0.7,
  },
  overlayLeft: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.6)',
  },
  scanArea: {
    width: width * 0.7,
    backgroundColor: 'transparent',
  },
  overlayRight: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.6)',
  },
  overlayBottom: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.6)',
  },
  scanFrame: {
    position: 'absolute',
    borderWidth: 2,
    borderColor: 'transparent',
  },
  corner: {
    position: 'absolute',
    width: 30,
    height: 30,
    borderColor: colors.primary.green,
    borderWidth: 3,
  },
  cornerTopLeft: {
    top: -2,
    left: -2,
    borderRightWidth: 0,
    borderBottomWidth: 0,
    borderTopLeftRadius: 8,
  },
  cornerTopRight: {
    top: -2,
    right: -2,
    borderLeftWidth: 0,
    borderBottomWidth: 0,
    borderTopRightRadius: 8,
  },
  cornerBottomLeft: {
    bottom: -2,
    left: -2,
    borderRightWidth: 0,
    borderTopWidth: 0,
    borderBottomLeftRadius: 8,
  },
  cornerBottomRight: {
    bottom: -2,
    right: -2,
    borderLeftWidth: 0,
    borderTopWidth: 0,
    borderBottomRightRadius: 8,
  },
  scanLine: {
    position: 'absolute',
    left: 0,
    right: 0,
    height: 2,
    backgroundColor: colors.primary.green,
    shadowColor: colors.primary.green,
    shadowOffset: {width: 0, height: 0},
    shadowOpacity: 0.8,
    shadowRadius: 4,
  },
  pulseEffect: {
    position: 'absolute',
    top: -10,
    left: -10,
    right: -10,
    bottom: -10,
    borderRadius: 8,
    borderWidth: 2,
    borderColor: colors.primary.green,
    backgroundColor: 'rgba(0, 200, 81, 0.1)',
  },
  statusIndicator: {
    position: 'absolute',
    top: 80,
    right: spacing.md,
    alignItems: 'center',
  },
  statusDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginBottom: spacing.xs,
  },
});

export default ScannerOverlay;



