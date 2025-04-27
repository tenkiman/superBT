      implicit none
      integer i,j,n
      integer IDIM,JDIM
      parameter(IDIM=3600, JDIM=1200)
CCCCC i=1    --> LON=0.05E
CCCCC i=100  --> LON=0.05+0.1*(100-1)
CCCCC j=1    --> LAT=59.95N
CCCCC j=JDIM --> LAT=59.95S

      real*4 rain(IDIM,JDIM)

      open(10,file=
     & 'gsmap_mvk.20211201.0000.v8.0000.0.dat',
     &     form='unformatted',access='direct',recl=4*IDIM*JDIM,
     &     status='old')

      read(10,rec=1)((rain(i,j),i=1,IDIM),j=1,JDIM) 

      close(10)

      do i=1,IDIM,1000
        do j=JDIM/2,JDIM/2
          write(*,*)i,j,rain(i,j)
        enddo
      enddo

      end
