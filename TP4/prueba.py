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


def recuperar_docID():

    with open('compressed_doc_ids.bin', 'rb') as binary_file:
        byte_data = binary_file.read()

  
    format_string = f">{len(byte_data)}B"
    unpacked_data = struct.unpack(format_string, byte_data)
    resultados = []
    docId = 0
    n = 1
    for data in unpacked_data:
        if data >=128:
            docId +=  data - 128 
            resultados.append(docId)
            docId = 0
            n = 1
        else:
            docId+= data * 128 * n 
            n +=1
    print(resultados)


def compress_index(index_filename):
    compressed_doc_ids_filename = "compressed_doc_ids.bin"
    compressed_freqs_filename = "compressed_frequencies.bin"
    compressed_index_filename = "compressed_index.bin"

    doc_ids = []
    freqs = []

    with open(index_filename, 'rb') as index_file:
        with open(compressed_index_filename, 'wb') as compressed_index_file:
            while True:
                data = index_file.read(8)
                if not data:
                    break
                doc_id, freq = struct.unpack('>II', data)
                compressed_index_file.write(struct.pack('>II', len(doc_ids), len(freqs)))
                doc_ids.append(doc_id)
                freqs.append(freq)
    

    with open(compressed_doc_ids_filename, 'wb') as doc_ids_file:
        for doc_id in doc_ids:
            array_data= (encode_vbyte(doc_id))
            byte_data = struct.pack(f">{len(array_data)}B", *array_data)
            doc_ids_file.write(byte_data)

    # with open(compressed_freqs_filename, 'wb') as freqs_file:
    #     for freq in freqs:
    #         freqs_file.write(encode_elias_gamma(freq))

    print("Índice comprimido y almacenado en archivos separados.")

compress_index('index.bin')
