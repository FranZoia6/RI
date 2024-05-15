import struct


def encode_vbyte(number):
    bytes_list = []
    while True:
        bytes_list.insert(0, number & 0x7F)
        number >>= 7
        if number == 0:
            break
    bytes_list[-1] |= 0x80  # Set the most significant bit of the last byte
    return bytes_list#bytes(bytes_list)


def decompress_docId(docIds_filename):

    with open(docIds_filename, 'rb') as binary_file:
        byte_data = binary_file.read()

    format_string = f">{len(byte_data)}B"
    unpacked_data = struct.unpack(format_string, byte_data)
    result = []
    docId = 0
    n = 1
    for data in unpacked_data:
        if data >=128:
            docId +=  data - 128 
            result.append(docId)
            docId = 0
            n = 1
        else:
            docId+= data * 128 * n 
            n +=1
    return result
    
def encode_elias_gamma(number):
    if number == 0:
        return '0'
    binary_representation = bin(number)[2:]  # Remove '0b' prefix
    offset = '0' * (len(binary_representation) - 1)
    return offset + binary_representation

def decode_elias_gamma(encoded_number):
    if encoded_number == '0':
        return 0
    length = 0
    while encoded_number[length] == '0':
        length += 1
    binary_representation = '1' + encoded_number[length+1:length*2+1]
    return int(binary_representation, 2)


def compress_index(index_filename):
    compressed_doc_ids_filename = "compressed_docIds.bin"
    compressed_freqs_filename = "compressed_frequencies.bin"

    doc_ids = []
    freqs = []

    with open(index_filename, 'rb') as index_file:
        while True:
            data = index_file.read(8)
            if not data:
                break
            doc_id, freq = struct.unpack('>II', data)
            doc_ids.append(doc_id)
            freqs.append(freq)
    

    with open(compressed_doc_ids_filename, 'wb') as doc_ids_file:
        for doc_id in doc_ids:
            array_data= encode_vbyte(doc_id)
            byte_data = struct.pack(f">{len(array_data)}B", *array_data)
            doc_ids_file.write(byte_data)

    # with open(compressed_freqs_filename, 'wb') as freqs_file:
    #     for freq in freqs:
    #         freqs_file.write(encode_elias_gamma(freq))

    print("Índice comprimido y almacenado en archivos separados.")

compress_index('index.bin')
#decompress_docId('compressed_docIds.bin')