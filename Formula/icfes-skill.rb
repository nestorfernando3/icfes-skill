class IcfesSkill < Formula
  desc "Skill para crear, revisar y exportar items estilo ICFES"
  homepage "https://github.com/nestor/icfes-skill"
  url "https://github.com/nestor/icfes-skill/archive/refs/tags/v0.1.0.tar.gz"
  version "0.1.0"
  sha256 "REEMPLAZAR_SHA256_DESPUES_DEL_RELEASE"
  license "MIT"

  def install
    libexec.install Dir["*"]
    bin.install_symlink libexec/"bin/icfes-skill" => "icfes-skill"
  end

  def caveats
    <<~EOS
      Instalar skill:
        icfes-skill install

      Global Codex:
        icfes-skill install --target codex --scope user

      Por proyecto:
        icfes-skill install --target codex --scope project --project /ruta/proyecto
    EOS
  end

  test do
    system bin/"icfes-skill", "doctor"
  end
end
