import streamlit as st
import socket
import dns.resolver


def get_ip_and_dns_records(domain_local):
    try:
        ip_local = socket.gethostbyname(domain_local)
    except socket.gaierror:
        ip_local = "Nu s-a putut rezolva IP-ul"

    dns_records_local = {}
    record_types = ['A', 'AAAA', 'MX', 'NS', 'CNAME', 'TXT', 'SOA']

    for record_type_local in record_types:
        try:
            answers = dns.resolver.resolve(domain_local, record_type_local)
            dns_records_local[record_type_local] = [str(rdata) for rdata in answers]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
            dns_records_local[record_type_local] = ["Nu există înregistrări"]

    return ip_local, dns_records_local


# Interfața Streamlit
st.title("DNS și IP Checker")

# Input pentru domeniu
domain = st.text_input("Introdu adresa site-ului (ex: example.com):")

# Când utilizatorul apasă butonul "Verifică"
if st.button("Verifică"):
    if domain:
        ip, dns_records = get_ip_and_dns_records(domain)
        st.subheader(f"Adresa IP pentru {domain}: {ip}")

        st.subheader("Înregistrări DNS:")
        for record_type, records in dns_records.items():
            st.write(f"**{record_type}**: {', '.join(records)}")
    else:
        st.error("Te rog introdu o adresă de site validă.")
