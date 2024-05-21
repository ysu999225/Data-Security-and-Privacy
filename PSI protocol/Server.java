import java.math.BigInteger;
import java.util.Random;

public class Server {
    public static void main(String[] args) 
    {
        Boolean debug=false;
    	if(args.length != 2) { System.out.println("Invalid arguments, exiting..."); return; }
    	
        String filename = args[0];
        String clientFilename = args[1];
	
        Inputs inputs = new Inputs(filename);

        BigInteger[] serverInputs = inputs.getInputs();

        BigInteger[] encryptedPolyCoeffs = (BigInteger[])StaticUtils.read(clientFilename);
        BigInteger publicKey = (BigInteger)StaticUtils. read("ClientPK.out");

        Paillier paillier = new Paillier();
        paillier.setPublicKey(publicKey);

        BigInteger[] encryptedPolyEval = new BigInteger[serverInputs.length];

        /* TODO: implement server-side protocol here.
         * For each sj in serverInputs:
			- Pick a random rj
			- Homomorphically evaluate P(sj)
			- Compute E_K(rj P(sj) + sj)
			- Set encryptedPolyEval[j] = E_K(rj P(sj) + sj)
        */
 	    // ------ Your code goes here. --------
        // server-side protocol

        // for eash sj pick a random rj
        for (int j = 0; j < serverInputs.length; j++) {
            BigInteger sj = serverInputs[j];
            // public void setPublicKey(BigInteger n)
            BigInteger rj = randomBigInt(paillier.n);
            // start with 0 (homo sum initial to 0)
            BigInteger homo = paillier.Encryption(BigInteger.ZERO);
            for (int i = 0; i < encryptedPolyCoeffs.length; i++) {
                // homo multiply encrypted coefficient sj^i (multiplication)
                // multiplication by a constant
                BigInteger term = paillier.const_mul(encryptedPolyCoeffs[i], sj.pow(i));
                // homo sum the terms(addition)
                //homomorphic addition
                homo = paillier.add(homo, term);
            }

            // E_k(rjP(s_j) + s_j)
            BigInteger rjP_sj = paillier.const_mul(homo, rj);
            BigInteger e_sj = paillier.Encryption(sj);
            encryptedPolyEval[j] = paillier.add(rjP_sj, e_sj);
        }

// Output the encrypted polynomial evaluations to a file
        StaticUtils.write(encryptedPolyEval, clientFilename + ".out");
    }


    //This is not cryptographically secure random number.
    public static BigInteger randomBigInt(BigInteger n) 
    {
        Random rand = new Random();
        BigInteger result = new BigInteger(n.bitLength(), rand);
        while( result.compareTo(n) >= 0 ) {
            result = new BigInteger(n.bitLength(), rand);
        }
        return result;
    }
}
