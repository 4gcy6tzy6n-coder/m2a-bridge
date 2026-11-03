# Cover letter（草稿——投稿前 owner 补作者信息）

To the Editors, Nature Machine Intelligence

We submit a cross-disciplinary study of the information requirements of feedback control under sensory latency, developed and tested across three domains: a control-model analysis, preregistered benchmarks in artificial delayed-control tasks, and constraint-setting tests on four public neural-behavioral datasets.

The core result is a bounded necessity map. In systematic elimination within a delayed feedback-control model, fresh current self-state in the closing loop is the fundamental necessary ingredient; gating of the delayed pathway is the substitute architecture when that pathway cannot receive fresh state; and delayed-only estimation — from extrapolation to observers whose internal loop embeds the transport delay — never rescued stability under our tests. We report honestly that two of our own earlier framings did not survive fair comparators: a classical controller with instantaneous state suffices once gating is in place, and granting fresh state to the delayed pathways removes the need for gating. The necessity claim is explicitly bounded to the model class and enumerated architectures.

The hierarchy then transferred, under frozen preregistration, to three non-biological control tasks where fresh-state feedback stayed stable through 600 ms of observation delay while delayed-observation controllers collapsed between 50 and 200 ms. For the machine-learning audience we contribute two further items: a quantified demonstration that state-dependent perturbation tests are defeated by behavioral autocorrelation — the same failure mode that afflicts offline and counterfactual evaluation on temporally correlated sequences — with an injection-recovery curve that states the procedure's detection floor; and a preregistration-first, negative-results-inclusive workflow used throughout and documented in full.

Every confirmatory analysis was preregistered with frozen files and SHA-256 hashes; inconclusive and negative results are reported as such, including one borderline signal (p=0.0503) whose post-result governance we disclose rather than dress up. We believe this is the right shape of contribution for an intelligent-systems audience: a design-relevant information hierarchy, its transfer, and evaluation methodology that other closed-loop fields can use — with limits stated rather than implied.

All data, analysis code, and preregistration hashes are listed in the Methods; the claim-evidence map accompanies the manuscript as supplementary material.

Sincerely,
[Corresponding author — owner to complete]
