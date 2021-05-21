/**
 * Gets the alphabet of characters used in a given string.
 * @param str The input string.
 * @returns The input string's alphabet as a character array.
 */
 function get_alphabet(str) {
    const Sigma = new Set();
    for (let i = 0; i < str.length; ++i)
        Sigma.add(str[i]);
    return Array.from(Sigma).sort();
}
/**
 * Gets the move-to-front indices for a given string and alphabet.
 * @param str The input string to be encoded.
 * @param Sigma The string's alphabet. Allowed to be specified since it could strictly contain all
 * the characters in the string.
 * @returns The move-to-front indices.
 */
function mtf(str, Sigma = null) {
    if (Sigma === null)
        Sigma = get_alphabet(str);
    const compressed = [];
    for (let i = 0; i < str.length; ++i) {
        const j = Sigma.indexOf(str[i]);
        compressed.push(j);
        Sigma.splice(j, 1);
        Sigma.unshift(str[i]);
    }
    return compressed;
}
/**
 * Encodes an integer with the Elias gamma code.
 * @param i The integer to encode.
 * @returns The encoded string.
 */
function gamma(i) {
    return ("0".repeat(Math.floor(Math.log2(i + 1)))).concat((i + 1).toString(2));
}
/**
 * Decodes a stream of Elias gamma codes into an array of integers.
 * @param bitstream A string of bits consisting of concatenated Elias gamma codes.
 * @returns The decoded numbers.
 */
function inv_gamma(bitstream) {
    const output = [];
    let j = 0;
    while ((j = bitstream.indexOf("1")) >= 0 && bitstream.length > 2 * j) {
        output.push(parseInt(bitstream.slice(j, 2 * j + 1), 2) - 1);
        bitstream = bitstream.slice(2 * j + 1);
    }
    if (bitstream.length > 0)
        return [];
    return output;
}
/**
 * Encodes a non-negative integer with the Elias delta code.
 * @param i The integer to encode.
 * @returns The encoded string.
 */
function delta(i) {
    const N = Math.floor(Math.log2(i + 1));
    const L = Math.floor(Math.log2(N + 1));
    const bin = (i + 1).toString(2).slice(1);
    return "0".repeat(L) + (N + 1).toString(2) + bin;
}
/**
 * Decodes a stream of Elias delta codes into an array of integers.
 * @param bitstream A string of bits consisting of concatenated Elias delta codes.
 * @returns The decoded numbers.
 */
function inv_delta(bitstream) {
    const output = [];
    let L = 0;
    while ((L = bitstream.indexOf("1")) >= 0) {
        if (bitstream.length < 2 * L + 1)
            return [];
        const N = parseInt(bitstream.slice(L, 2 * L + 1), 2) - 1;
        if (bitstream.length < 2 * L + 1 + N)
            return [];
        output.push(parseInt("1" + bitstream.slice(2 * L + 1, 2 * L + 1 + N), 2) - 1);
        bitstream = bitstream.slice(2 * L + N + 1);
    }
    if (bitstream.length > 0)
        return [];
    return output;
}
/**
 * Gets the ending indices of the Lyndon factors for a given string, by Duval's algorithm.
 * @param str The input string.
 * @returns The Lyndon factorization of the input string.
 */
function lyndon(str) {
    const fact = [-1];
    let k = -1;
    while (k < str.length - 1) {
        let i = k + 1, j = k + 2;
        while (j < str.length && str[i] <= str[j]) {
            if (str[i] === str[j]) {
                i += 1;
                j += 1;
            }
            else {
                i = k + 1;
                j += 1;
            }
        }
        do {
            k = k + j - i;
            fact.push(k);
        } while (k < i);
    }
    return fact;
}
/**
 * Gets all of the cyclic rotations of a given segment.
 * @param segment The input segment.
 * @returns The cyclic rotations of the input segment.
 */
function get_segment_rotations(segment) {
    const rots = [];
    for (let i = segment.start; i <= segment.end; ++i) {
        rots.push({
            start: i,
            end: segment.end,
            restart: segment.start,
        });
    }
    return rots;
}
/**
 * Gets the comparator function which allows for comparing Segments of a given string in the
 * lexicographic infinite periodic order.
 * @param str The string whose segments are to be compared.
 * @returns The Segment comparator function on the input string.
 */
function get_periodic_comparator(str) {
    return (i, j) => {
        let i_it = i.start, j_it = j.start;
        do {
            if (str[i_it] < str[j_it])
                return -1;
            else if (str[i_it] > str[j_it])
                return 1;
            i_it++;
            if (i_it > i.end)
                i_it = i.restart;
            j_it++;
            if (j_it > j.end)
                j_it = j.restart;
            // Declare a tie if we ever return to the origin.
        } while (!(i_it === i.start && j_it === j.start));
        return 0;
    };
}
/**
 * Computes the Gil-Scott bijective Burrows-Wheeler transform of the input string.
 * @param str The string to be transformed.
 * @returns The Gil-Scott BWT of the input string.
 */
function bwt(str) {
    // Collect the indices of rotations of the Lyndon factors.
    const lyndon_fact = lyndon(str);
    const lyndon_fact_segments = [];
    for (let i = 0; i < lyndon_fact.length - 1; ++i)
        lyndon_fact_segments.push({
            start: lyndon_fact[i] + 1,
            end: lyndon_fact[i + 1],
            restart: lyndon_fact[i] + 1,
        });
    const rotations = [];
    for (const fact of lyndon_fact_segments) {
        for (const rot of get_segment_rotations(fact))
            rotations.push(rot);
    }
    // The final result consists of the concatenated last rotation of each Lyndon factor.
    // It is an open problem to do this step in faster than O(n log n) time.
    const output = [];
    rotations.sort(get_periodic_comparator(str));
    for (const rot of rotations) {
        if (rot.start === rot.restart) {
            output.push(str[rot.end]);
        }
        else {
            output.push(str[rot.start - 1]);
        }
    }
    return output.join("");
}
/**
 * Inverts an array of unique characers into a map of characters to their indices in the array.
 * @param Sigma The array to be inverted.
 * @returns The inverted map.
 */
function get_char_map(Sigma) {
    const char_map = new Map();
    for (let i = 0; i < Sigma.length; ++i)
        char_map[Sigma[i]] = i;
    return char_map;
}
/**
 * Performs the subroutine `Match` from the Gil & Scott Burrows-Wheeler transform paper.
 * @param str A string.
 * @param Sigma The alphabet of the input string.
 * @returns The output permutation.
 */
function match(str, Sigma) {
    const theta = [];
    const char_map = get_char_map(Sigma);
    const counts = Array(Sigma.length).fill(0);
    for (let i = 0; i < str.length; ++i)
        counts[char_map[str[i]]] += 1;
    const before = Array(Sigma.length).fill(0);
    for (let i = 1; i < Sigma.length; ++i)
        before[i] = before[i - 1] + counts[i - 1];
    const seen = Array(Sigma.length).fill(0);
    for (let i = 0; i < str.length; ++i) {
        theta.push(before[char_map[str[i]]] + seen[char_map[str[i]]]);
        seen[char_map[str[i]]] += 1;
    }
    return theta;
}
/**
 * Performs the subroutine `MultiThread` from the Gil & Scott Burrows-Wheeler transform paper.
 * @param str A string.
 * @param theta A permutation.
 * @returns The output string.
 */
function multithread(str, theta) {
    const T = theta.slice();
    const alpha = [];
    for (let j = 0; j < str.length; ++j) {
        if (T[j] !== -1) {
            let k = j;
            do {
                alpha.push(str[k]);
                const t = k;
                k = T[k];
                T[t] = -1;
            } while (T[k] !== -1);
        }
    }
    return alpha.reverse().join("");
}
/**
 * Inverts the Gil-Scott bijective Burrows-Wheeler transform of a given string.
 * @param str The string to transform.
 * @returns The inverted BWT of the given string.
 */
function inv_bwt(str) {
    const Sigma = get_alphabet(str);
    const theta = match(str, Sigma);
    return multithread(str, theta);
}
/**
 * Decodes a move-to-front stream of bits given an alphabet.
 * @param bitstream The input bit stream.
 * @param Sigma The alphabet of the coded string.
 * @returns The decoded string.
 */
function inv_mtf(bitstream, Sigma) {
    const data = inv_delta(bitstream);
    if (data === null || Math.max(...data) >= Sigma.length)
        return "";
    const decoded = [];
    for (let i = 0; i < data.length; ++i) {
        const j = data[i];
        const c = Sigma[j];
        decoded.push(c);
        Sigma.splice(j, 1);
        Sigma.unshift(c);
    }
    return decoded.join("");
}

