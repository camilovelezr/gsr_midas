using CordraClient
using ProgressBars
using JSON

print("Local? (y/n) ")
l = readline()

if l == "y"
    host = "https://localhost:8443"
    username = "admin"
else
    host = "https://sandbox.materialhub.org"
    username="camilovelezr"
end

cc = CordraConnection(host, username, verify = false)

r = find_object(cc, "/CamiloExplore:1"; ids = true, pageSize = -1)

@time begin
    Threads.@threads for id in ProgressBar(r["results"])
        delete_object(cc, id)
    end
end

#@JSON read_object(cc, "test/gsr-2019-40c6/mllsq_generic_gsr")

