#!/usr/bin/awk -f

# Formato: timestamp nivel servico mensagem livre
NF >= 3 {
    level = $2
    service = $3
    if (!(level in seen_level)) {
        level_order[++level_count] = level
        seen_level[level] = 1
    }
    if (!(service in seen_service)) {
        service_order[++service_count] = service
        seen_service[service] = 1
    }
    by_level[level]++
    by_service[service]++
    total++
}

END {
    print "total=" total
    for (i = 1; i <= level_count; i++) {
        level = level_order[i]
        print "level." level "=" by_level[level]
    }
    for (i = 1; i <= service_count; i++) {
        service = service_order[i]
        print "service." service "=" by_service[service]
    }
}
