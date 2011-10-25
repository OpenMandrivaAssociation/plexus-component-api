%define project_version 1.0-alpha-15

Name:           plexus-component-api
Version:        1.0
Release:        0.6.alpha15
Summary:        Plexus Component API

Group:          Development/Java
License:        ASL 2.0
URL:            http://svn.codehaus.org/plexus/plexus-containers/tags/plexus-containers-1.0-alpha-15/plexus-component-api/
#svn export http://svn.codehaus.org/plexus/plexus-containers/tags/plexus-containers-1.0-alpha-15/plexus-component-api/ plexus-component-api-1.0-alpha-15
#tar zcf plexus-component-api-1.0-alpha-15.tar.gz plexus-component-api-1.0-alpha-15/
Source0:        plexus-component-api-1.0-alpha-15.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

BuildRequires:  java-devel >= 0:1.6.0
BuildRequires:  jpackage-utils >= 0:1.7.2
BuildRequires:  ant, ant-nodeps
BuildRequires:  maven2 >= 0:2.0.4-9
BuildRequires:  maven2-plugin-assembly
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-resources
BuildRequires:  maven2-plugin-site
BuildRequires:  maven2-plugin-plugin
BuildRequires:  maven-surefire-maven-plugin
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  maven2-plugin-javadoc
BuildRequires:  maven-doxia
BuildRequires:  maven-doxia-sitetools
BuildRequires:  plexus-digest
BuildRequires:  plexus-classworlds

Requires:          java-devel >= 0:1.6.0
Requires:          plexus-digest
Requires:          plexus-classworlds
Requires:          jpackage-utils
Requires(post):    jpackage-utils >= 0:1.7.2
Requires(postun):  jpackage-utils >= 0:1.7.2

%description
Plexus Component API

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.


%prep
%setup -q -n %{name}-%{project_version}

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mvn-jpp \
        -e \
        -Dmaven2.jpp.mode=true \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        install javadoc:javadoc

%install

rm -rf %{buildroot}

# jars
install -d -m 0755 %{buildroot}%{_javadir}/plexus
install -m 644 target/%{name}-%{project_version}.jar %{buildroot}%{_javadir}/plexus

(cd %{buildroot}%{_javadir}/plexus && for jar in *-%{project_version}*; \
    do ln -sf ${jar} `echo $jar| sed "s|-%{project_version}||g"`; done)

%add_to_maven_depmap org.codehaus.plexus %{name} %{project_version} JPP/plexus %{name}

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP.plexus-%{name}.pom

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/plexus/%{name}-%{version}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/plexus/%{name}-%{version}/
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/plexus/%{name}
rm -rf target/site/api*

%post
%update_maven_depmap

%postun
%update_maven_depmap

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_javadir}/plexus/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/plexus/%{name}-%{version}
%{_javadocdir}/plexus/%{name}

