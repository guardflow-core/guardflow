import { useState, useEffect } from 'react';
import { ethers } from 'ethers';

declare global {
  interface Window {
    ethereum: any;
  }
}

interface WalletState {
  address: string | null;
  chainId: string | null;
  isConnected: boolean;
}

export function useWallet() {
  const [wallet, setWallet] = useState<WalletState>({
    address: null,
    chainId: null,
    isConnected: false,
  });

  const connect = async () => {
    if (typeof window.ethereum !== 'undefined') {
      try {
        const provider = new ethers.BrowserProvider(window.ethereum);
        const accounts = await provider.send("eth_requestAccounts", []);
        const network = await provider.getNetwork();
        
        setWallet({
          address: accounts[0],
          chainId: network.chainId.toString(),
          isConnected: true,
        });
      } catch (error) {
        console.error("Error connecting wallet:", error);
      }
    } else {
      alert("Please install MetaMask!");
    }
  };

  useEffect(() => {
    if (typeof window.ethereum !== 'undefined') {
      window.ethereum.on('accountsChanged', (accounts: string[]) => {
        setWallet(prev => ({
          ...prev,
          address: accounts[0] || null,
          isConnected: !!accounts.length,
        }));
      });
    }
  }, []);

  return { ...wallet, connect };
}
