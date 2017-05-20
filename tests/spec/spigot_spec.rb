describe user 'spigot' do
  it { should exist }
end

describe group 'spigot' do
  it { should exist }
end

describe file '/srv/spigot' do
  it {
    should be_directory
    should be_owned_by 'spigot'
    should be_grouped_into 'spigot'
  }
end

describe file '/srv/spigot/build/spigot-1.9.jar' do
  it {
    should be_file
    should be_owned_by 'spigot'
    should be_grouped_into 'spigot'
  }
end

describe file '/srv/spigot/spigot.jar' do
  it {
    should be_symlink
    should be_linked_to '/srv/spigot/build/spigot-1.9.jar'
  }
end

describe file '/srv/spigot/eula.txt' do
  its(:content) { should match 'true' }
end

java = case os[:name]
       when 'centos' then 'java-1.8.0-openjdk'
       when 'debian' then 'openjdk-8-jdk'
       else 'default-jdk'
       end

describe package java do
  it { should be_installed }
end

describe processes(Regexp.new("java -Xmx1024M -Xms1024M -jar spigot.jar nogui")) do
  its('users') { should cmp 'spigot' }
end

describe port(25565) do
  it { should be_listening }
end

describe port(25564) do
  it { should be_listening }
end

expected_hook_log = <<EOF
before_setup
after_setup
before_download
after_download
before_install
after_install
before_start
after_start
EOF

describe file '/tmp/hooks' do
  its(:content) { should eq expected_hook_log }
end
