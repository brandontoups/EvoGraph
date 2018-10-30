

# Algorithm 1 : gsaNA(G1,G2,G3)

# µ ← µa, µp ← ∅
# a ← |S1 | ▷ Initialize a as the size of the anchors set
# k ← 3 ▷ Initialize k number of top similar vertices per vertex
# n ← 20 ▷ Initialize maximum number of iterations
# ϵ ← 1.02 ▷ Minimum changes for next iteration
# while (n > 0) and ( |µ | / |µp | > ϵ) do
#   µp ← µ ▷ Store current mapping in µp
#    ▷ Computation of shortest paths from seed anchors
#   for each u ∈ S1 do
#       ▷ For each “new” seed anchor perform a BFS
#       if δ (u, .) is not computed before then
#           δ (u, .) ← BF S(G1, u), δ (µ[u], .) ← BF S(G2, µ[u])
#   SC ← findCentralAnchors(G1, S1, δ, 1)
#   SV ← findVantageAnchors(S1 \ SC, SC, δ )
#   OV ←pairAndOrder(SV , δ )
#   Q ← QTree((−1, 1), (1, −1))
#   T ← insertVertices(V1 ∪ V2, OV , Q, δ )
#   P ← topSimilars(T, k, σ )
#   µ ← map(P, µ, σ )
#    ▷ Append highest similar vertices as new new anchors
#   if a > 1000 then
#       S1 = {u : µa[u] = v }
#       a ← |S1 |
#   for i = 1 to a do
#       S1 ∪ {u }, where u ← argmaxu∈V1\S1 σ (u, v)
#   a ← 2 × a
#   n ← n − 1
# return µ
def gsaNA():
    


if __name__ == '__main__':
    gsaNA()